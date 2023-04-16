# application for creating beatmap from input audio
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

from MapCreator.music.model_onset_detect import build_model_default, build_model_superflux, build_model_beat, \
    build_model_plp, build_model_plp_log

LARGEFONT = ("Verdana", 15)


class ProjectPresentation(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="presentation", font=LARGEFONT)
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label = ttk.Label(self, text="Project consist of...", font=LARGEFONT)
        label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        label = ttk.Label(self, text="README", font=LARGEFONT)
        label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        label = ttk.Label(self, text="DISCLAIMER (made by students)", font=LARGEFONT)
        label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        label = ttk.Label(self, text="Version (osu file format v14)", font=LARGEFONT)
        label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        label = ttk.Label(self, text="LICENSE go see GNU or MIT for license", font=LARGEFONT)
        label.grid(row=5, column=0, padx=10, pady=10, sticky="w")


insert_text = """Models de test :
beatmaps réalisées à partir de l'analyse des onsets et de la structure rhythmique d'une piste audio.
les position x et y sont aléatoire.
modèle peut précis ne prenant pas en compte la difficultés.

 - traditional onset methods : able to detect quite a bit of the structure for simple sound. for music with a more complex structure, 
 with many instruments + voice + soft sound, it has a hard time to detect the onet , work base on peak selection strategy
 see doc for more onformation : https://...
 
 - superflux onset methods
 see documentation for more details : http...
 
 - beat : to repetitve, difficulty depend too much on its speed
 
 - Predominant Local Pulse (PLP) some sort of bpm depending on the time frame in the music,
 
 - PLP log-normal, another way to visualize PLP
 
 -  novelty curve?
 
#proof of concept
"""


class ModelTest(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Model test")
        label.grid(row=0, column=2, padx=10, pady=10)

        # audio path
        location = ""

        # Audio frame
        label_audio = tk.Label(self, text=" Audio :", width=6)
        label_audio.grid(row=1, column=0, padx=5, pady=5)
        self.string_var_audio_path = tk.StringVar()
        entry_audio = tk.Entry(self, textvariable=self.string_var_audio_path, width=55)
        entry_audio.grid(row=1, column=1, columnspan=3, sticky=tk.W + tk.E)
        entry_audio.insert(0, self.location)
        self.string_var_audio_path.set(location)
        btn_browse_file = tk.Button(self, text="Browse audio",
                                    command=lambda: self.browse_file(self.string_var_audio_path))
        btn_browse_file.grid(row=1, column=4, sticky=tk.W + tk.E)

        # dir path
        location = ""

        # Dir frame
        label_dir = tk.Label(self, text=" Project dir :")
        label_dir.grid(row=2, column=0, padx=5, pady=5)
        self.string_var_dir_path = tk.StringVar()
        entry_dir = tk.Entry(self, textvariable=self.string_var_dir_path, width=55)
        entry_dir.grid(row=2, column=1, columnspan=3, sticky=tk.W + tk.E)
        entry_dir.insert(0, self.location)
        self.string_var_dir_path.set(location)
        btn_browse_folder = tk.Button(self, text="Browse folder",
                                      command=lambda: self.browse_folder(self.string_var_dir_path))
        btn_browse_folder.grid(row=2, column=4, sticky=tk.W + tk.E)

        # description
        label_description = tk.Label(self, text="Description")
        label_description.grid(row=3, column=0)

        text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                              width=80, height=15)

        text_area.grid(column=0, row=4, columnspan=5, sticky=tk.W + tk.E)
        text_area.insert(tk.END, insert_text)
        text_area.config(state=tk.DISABLED)

        # project repo path entry?
        # create project folder?
        # new project?
        # existing project?

        # btn
        btn_create_default_onset = tk.Button(self, text="default onset method",
                                             command=lambda: self.create(self.string_var_audio_path.get(),
                                                                         self.string_var_dir_path.get(),
                                                                         build_model_default))
        btn_create_default_onset.grid(row=5, column=0, columnspan=2, sticky=tk.W + tk.E)

        btn_create_superflux_onset = tk.Button(self, text="superflux onset method",
                                               command=lambda: self.create(self.string_var_audio_path.get(),
                                                                           self.string_var_dir_path.get(),
                                                                           build_model_superflux))
        btn_create_superflux_onset.grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E)

        btn_create_beat = tk.Button(self, text="beatmap based on bpm method",
                                    command=lambda: self.create(self.string_var_audio_path.get(),
                                                                self.string_var_dir_path.get(), build_model_beat))
        btn_create_beat.grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E)

        btn_create_plp = tk.Button(self, text="plp method",
                                   command=lambda: self.create(self.string_var_audio_path.get(),
                                                               self.string_var_dir_path.get(), build_model_plp))
        btn_create_plp.grid(row=5, column=2, columnspan=2, sticky=tk.W + tk.E)

        btn_create_plp_log = tk.Button(self, text="plp log method",
                                       command=lambda: self.create(self.string_var_audio_path.get(),
                                                                   self.string_var_dir_path.get(), build_model_plp_log))
        btn_create_plp_log.grid(row=6, column=2, columnspan=2, sticky=tk.W + tk.E)

    def browse_file(self, var):
        filename = filedialog.askopenfilename(initialdir="",
                                              title="Select a File",
                                              filetypes=(("all files", "*.*"), ("Text files", "*.txt*")))
        var.set(filename)

    def browse_folder(self, var):
        filename = filedialog.askdirectory(initialdir="",
                                           title="Select a Folder")
        var.set(filename)

    def create(self, audio_path, dir_path, fonction):
        if audio_path == "" or dir_path == "":
            print("# error message")
            pass
        else:
            fonction(audio_path, dir_path)
