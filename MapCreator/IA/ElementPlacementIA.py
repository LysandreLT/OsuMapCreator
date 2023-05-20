import math
import tensorflow as tf
from keras_cv.models.stable_diffusion.diffusion_model import ResBlock, SpatialTransformer, Upsample
from tensorflow import keras
import numpy as np
from keras_cv.models.stable_diffusion.__internal__.layers.padded_conv2d import (
    PaddedConv2D,
)
from keras_cv.models.stable_diffusion.constants import _ALPHAS_CUMPROD

"""
Unet, deeplearning
Entrées : .txt, .MP3 (x minutes max)
Sortie : .txt
"""

# Fonctions


class DiffusionModel(keras.Model):
    def __init__(
            self,
            maxBeatmapSize,
            maxAudioSize,
            name=None,
            download_weights=False,
    ):
        context = keras.layers.Input((maxAudioSize, 2))
        t_embed_input = keras.layers.Input((320,))
        latent = keras.layers.Input((maxBeatmapSize, 2, 2))

        t_emb = keras.layers.Dense(1280)(t_embed_input)
        t_emb = keras.layers.Activation("swish")(t_emb)
        t_emb = keras.layers.Dense(1280)(t_emb)

        # Downsampling flow

        outputs = []
        x = PaddedConv2D(320, kernel_size=3, padding=1)(latent)
        outputs.append(x)

        for _ in range(2):
            x = ResBlock(320)([x, t_emb])
            x = SpatialTransformer(5, 64, fully_connected=True)([x, context])
            outputs.append(x)
        x = PaddedConv2D(320, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        for _ in range(2):
            x = ResBlock(640)([x, t_emb])
            x = SpatialTransformer(10, 64, fully_connected=True)([x, context])
            outputs.append(x)
        x = PaddedConv2D(640, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        for _ in range(2):
            x = ResBlock(1280)([x, t_emb])
            x = SpatialTransformer(20, 64, fully_connected=True)([x, context])
            outputs.append(x)
        x = PaddedConv2D(1280, 3, strides=2, padding=1)(x)  # Downsample 2x
        outputs.append(x)

        for _ in range(2):
            x = ResBlock(1280)([x, t_emb])
            outputs.append(x)

        # Middle flow

        x = ResBlock(1280)([x, t_emb])
        x = SpatialTransformer(20, 64, fully_connected=True)([x, context])
        x = ResBlock(1280)([x, t_emb])

        # Upsampling flow

        for _ in range(3):
            x = keras.layers.Concatenate()([x, outputs.pop()])
            x = ResBlock(1280)([x, t_emb])
        x = Upsample(1280)(x)

        for _ in range(3):
            x = keras.layers.Concatenate()([x, outputs.pop()])
            x = ResBlock(1280)([x, t_emb])
            x = SpatialTransformer(20, 64, fully_connected=True)([x, context])
        x = Upsample(1280)(x)

        for _ in range(3):
            x = keras.layers.Concatenate()([x, outputs.pop()])
            x = ResBlock(640)([x, t_emb])
            x = SpatialTransformer(10, 64, fully_connected=True)([x, context])
        x = Upsample(640)(x)

        for _ in range(3):
            x = keras.layers.Concatenate()([x, outputs.pop()])
            x = ResBlock(320)([x, t_emb])
            x = SpatialTransformer(5, 64, fully_connected=True)([x, context])

        # Exit flow

        x = keras.layers.GroupNormalization(epsilon=1e-5)(x)
        x = keras.layers.Activation("swish")(x)
        output = PaddedConv2D(4, kernel_size=3, padding=1)(x)

        super().__init__([latent, t_embed_input, context], output, name=name)

        if download_weights:
            diffusion_model_weights_fpath = keras.utils.get_file(
                origin="https://huggingface.co/ianstenbit/keras-sd2.1/resolve/main/diffusion_model_v2_1.h5",
                # noqa: E501
                file_hash="c31730e91111f98fe0e2dbde4475d381b5287ebb9672b1821796146a25c5132d",  # noqa: E501
            )
            self.load_weights(diffusion_model_weights_fpath)


# Modèle
class ElementPlacement:
    def __init__(
            self,
            maxBeatmapSize,
            maxAudioSize
    ):

        self.maxBeatmapSize = maxBeatmapSize
        self.maxAudioSize = maxAudioSize

        # lazy initialize the component models and the tokenizer
        self._diffusion_model = None

    def generate_beatmap(
            self,
            encoded_music,
            batch_size=1,
            num_steps=50,
            unconditional_guidance_scale=7.5,
            diffusion_noise=None,
            seed=None,
    ):
        """Generates a beatmap based on encoded music.

        The encoding passed to this method should be derived from
        `StableDiffusion.encode_music`.

        Args:
            encoded_music: Tensor of shape (`batch_size`, 77, 768), or a Tensor
                of shape (77, 768). When the batch axis is omitted, the same
                encoded text will be used to produce every generated image.
            batch_size: int, number of images to generate, defaults to 1.
            num_steps: int, number of diffusion steps (controls beatmap quality),
                defaults to 50.
            unconditional_guidance_scale: float, controlling how closely the
                image should adhere to the prompt. Larger values result in more
                closely adhering to the prompt, but will make the image noisier.
                Defaults to 7.5.
            diffusion_noise: Tensor of shape (`batch_size`, img_height // 8,
                img_width // 8, 4), or a Tensor of shape (img_height // 8,
                img_width // 8, 4). Optional custom noise to seed the diffusion
                process. When the batch axis is omitted, the same noise will be
                used to seed diffusion for every generated image.
            seed: integer which is used to seed the random generation of
                diffusion noise, only to be specified if `diffusion_noise` is
                None.

        Example:

        ```python
        from keras_cv.models import StableDiffusion

        batch_size = 8
        model = StableDiffusion(img_height=512, img_width=512, jit_compile=True)
        e_tacos = model.encode_text("Tacos at dawn")
        e_watermelons = model.encode_text("Watermelons at dusk")

        e_interpolated = tf.linspace(e_tacos, e_watermelons, batch_size)
        images = model.generate_image(e_interpolated, batch_size=batch_size)
        ```
        """
        if diffusion_noise is not None and seed is not None:
            raise ValueError(
                "`diffusion_noise` and `seed` should not both be passed to "
                "`generate_image`. `seed` is only used to generate diffusion "
                "noise when it's not already user-specified."
            )

        context = self._expand_tensor(encoded_music, batch_size)

        if diffusion_noise is not None:
            diffusion_noise = tf.squeeze(diffusion_noise)
            if diffusion_noise.shape.rank == 3:
                diffusion_noise = tf.repeat(
                    tf.expand_dims(diffusion_noise, axis=0), batch_size, axis=0
                )
            latent = diffusion_noise
        else:
            latent = self._get_initial_diffusion_noise(batch_size, seed)

        # Iterative reverse diffusion stage
        timesteps = tf.range(1, 1000, 1000 // num_steps)
        alphas, alphas_prev = self._get_initial_alphas(timesteps)
        progbar = keras.utils.Progbar(len(timesteps))
        iteration = 0
        for index, timestep in list(enumerate(timesteps))[::-1]:
            latent_prev = latent  # Set aside the previous latent vector
            t_emb = self._get_timestep_embedding(timestep, batch_size)

            latent = self.diffusion_model.predict_on_batch(
                [latent, t_emb, context]
            )

            a_t, a_prev = alphas[index], alphas_prev[index]
            pred_x0 = (latent_prev - math.sqrt(1 - a_t) * latent) / math.sqrt(
                a_t
            )
            latent = (
                    latent * math.sqrt(1.0 - a_prev) + math.sqrt(a_prev) * pred_x0
            )
            iteration += 1
            progbar.update(iteration)

        # Decoding stage
        decoded = self.decoder.predict_on_batch(latent)
        decoded = ((decoded + 1) / 2) * 255
        return np.clip(decoded, 0, 255).astype("uint8")

    def _expand_tensor(self, text_embedding, batch_size):
        """Extends a tensor by repeating it to fit the shape of the given batch
        size."""
        text_embedding = tf.squeeze(text_embedding)
        if text_embedding.shape.rank == 2:
            text_embedding = tf.repeat(
                tf.expand_dims(text_embedding, axis=0), batch_size, axis=0
            )
        return text_embedding

    @property
    def diffusion_model(self):
        """diffusion_model returns the diffusion model with pretrained weights.
                Can be overriden for tasks where the diffusion model needs to be
                modified.
                """
        if self._diffusion_model is None:
            self._diffusion_model = DiffusionModel(
                self.maxBeatmapSize, self.maxAudioSize
            )
        return self._diffusion_model

    def _get_timestep_embedding(
            self, timestep, batch_size, dim=320, max_period=10000
    ):
        half = dim // 2
        freqs = tf.math.exp(
            -math.log(max_period) * tf.range(0, half, dtype=tf.float32) / half
        )
        args = tf.convert_to_tensor([timestep], dtype=tf.float32) * freqs
        embedding = tf.concat([tf.math.cos(args), tf.math.sin(args)], 0)
        embedding = tf.reshape(embedding, [1, -1])
        return tf.repeat(embedding, batch_size, axis=0)

    def _get_initial_alphas(self, timesteps):
        alphas = [_ALPHAS_CUMPROD[t] for t in timesteps]
        alphas_prev = [1.0] + alphas[:-1]

        return alphas, alphas_prev

    def _get_initial_diffusion_noise(self, batch_size, seed):
        if seed is not None:
            return tf.random.stateless_normal(
                (batch_size, 20000, 2, 2),
                seed=[seed, seed],
            )
        else:
            return tf.random.normal(
                (batch_size, 2000, 2, 2)
            )
