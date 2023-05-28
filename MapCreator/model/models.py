# import the necessary packages
from keras.engine.input_layer import InputLayer
from keras.models import Sequential
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Input
from keras.models import Model
from keras.layers import concatenate


def create_mlp(dim, regress=False):
    # define our MLP network
    model = Sequential()
    model.add(Dense(32, input_dim=dim, activation="relu"))
    model.add(Dense(32, activation="relu"))
    # check to see if the regression node should be added
    if regress:
        model.add(Dense(32, activation="linear"))
    # return our model
    return model


def create_difficulty(shape):
    input2 = InputLayer(input_shape=shape)
    model = Model(input2)
    return model


def create_cnn(width, height, depth, filters=(16, 32, 64, 128, 256), regress=False):
    # initialize the input shape and channel dimension, assuming
    # TensorFlow/channels-last ordering
    inputShape = (height, width, depth)
    chanDim = -1
    # define the model input
    inputs = Input(shape=inputShape)
    # loop over the number of filters
    for (i, f) in enumerate(filters):
        # if this is the first CONV layer then set the input
        # appropriately
        if i == 0:
            x = inputs
        # CONV => RELU => BN => POOL
        x = Conv2D(f, (3, 3), padding="same")(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = MaxPooling2D(pool_size=(2, 2))(x)

        # flatten the volume, then FC => RELU => BN => DROPOUT
        x = Flatten()(x)
        x = Dense(64)(x)
        x = Activation("relu")(x)
        x = BatchNormalization(axis=chanDim)(x)
        x = Dropout(0.5)(x)
        # apply another FC layer, this one to match the number of nodes
        # coming out of the MLP
        x = Dense(32)(x)
        x = Activation("relu")(x)
        # check to see if the regression node should be added
        if regress:
            x = Dense(16, activation="linear")(x)
        # construct the CNN
        model = Model(inputs, x)
        # return the CNN
        return model


def get_model(trainAttrX_shape, trainDiffX_shape):
    # create the MLP and CNN models
    mlp = create_mlp(trainAttrX_shape, regress=False)
    cnn = create_cnn(64, 64, 3, regress=False)
    diff = create_difficulty(trainDiffX_shape)
    # create the input to our final set of layers as the *output* of both
    # the MLP and CNN
    combinedInput = concatenate([mlp.output, cnn.output, diff.output])

    x = Dense(64, activation="relu")(combinedInput)
    x = Dense(32, activation="linear")(x)
    # our final model will accept music spectrogram image/difficulty data on the MLP
    # input and images on the CNN input, outputting an array of the same dim as the input of the MLP
    model = Model(inputs=[cnn.input, diff.input], outputs=mlp.input)
    return model
