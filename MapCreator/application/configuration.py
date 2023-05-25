import tkinter as tk
from tkinter import ttk


class TabGeneral(tk.Frame):

    def __init__(self, master, project):
        tk.Frame.__init__(self, master)

        song_and_map_metadata_info_frame = tk.LabelFrame(self, text="Song and Map Metadata")
        song_and_map_metadata_info_frame.grid(row=0, column=0, padx=20, pady=20)

        # Labels
        label_artist = tk.Label(song_and_map_metadata_info_frame, text="Artist")
        label_artist.grid(row=0, column=0, sticky="E")
        label_romanised_artist = tk.Label(song_and_map_metadata_info_frame, text="Romanised Artist")
        label_romanised_artist.grid(row=1, column=0, sticky="E")
        label_title = tk.Label(song_and_map_metadata_info_frame, text="Title")
        label_title.grid(row=2, column=0, sticky="E")
        label_romanised_title = tk.Label(song_and_map_metadata_info_frame, text="Romanised Title")
        label_romanised_title.grid(row=3, column=0, sticky="E")
        label_beatmap_creator = tk.Label(song_and_map_metadata_info_frame, text="Beatmap Creator")
        label_beatmap_creator.grid(row=4, column=0, sticky="E")
        label_difficulty = tk.Label(song_and_map_metadata_info_frame, text="Difficulty")
        label_difficulty.grid(row=5, column=0, sticky="E")
        label_source = tk.Label(song_and_map_metadata_info_frame, text="Source")
        label_source.grid(row=6, column=0, sticky="E")
        label_tags = tk.Label(song_and_map_metadata_info_frame, text="Tags")
        label_tags.grid(row=7, column=0, sticky="E")

        # Entry
        # Artist
        self.artist_textvar = tk.StringVar()
        self.artist_textvar.set(project.metadata.Artist)
        entry_artist = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.artist_textvar)
        entry_artist.grid(row=0, column=1, sticky="EW")
        # Romanised Artist
        self.romanised_artist_textvar = tk.StringVar()
        self.romanised_artist_textvar.set(project.metadata.ArtistUnicode)
        entry_romanised_artist = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.romanised_artist_textvar)
        entry_romanised_artist.grid(row=1, column=1, sticky="EW")
        # Title
        self.title_textvar = tk.StringVar()
        self.title_textvar.set(project.metadata.Title)
        entry_title = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.title_textvar)
        entry_title.grid(row=2, column=1, sticky="EW")
        # Romanised Title
        self.romanised_title_textvar = tk.StringVar()
        self.romanised_title_textvar.set(project.metadata.TitleUnicode)
        entry_romanised_title = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.romanised_title_textvar)
        entry_romanised_title.grid(row=3, column=1, sticky="EW")
        # Beatmap creator
        self.creator_textvar = tk.StringVar()
        self.creator_textvar.set(project.metadata.Creator)
        entry_beatmap_creator = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.creator_textvar)
        entry_beatmap_creator.grid(row=4, column=1, sticky="EW")
        # difficulty
        self.difficulty_values = ["", "Easy", "Normal", "Hard", "Insane"]
        self.difficulty_textvar = tk.StringVar()
        combobox_difficulty = ttk.Combobox(song_and_map_metadata_info_frame,
                                           values=self.difficulty_values, textvariable=self.difficulty_textvar)
        combobox_difficulty.grid(row=5, column=1, sticky="EW")
        # if project.metadata.Version in self.difficulty_values:
        #     difficulty_textvar.set(project.metadata.Version)
        #
        # else:
        #     self.difficulty_values.append(project.metadata.Version)
        #     difficulty_textvar.set(project.metadata.Version)
        #     print(combobox_difficulty.current())

        # Source
        self.source_textvar = tk.StringVar()
        self.source_textvar.set(project.metadata.Source)
        entry_source = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.source_textvar)
        entry_source.grid(row=6, column=1, sticky="EW")
        # Tags
        self.tags_textvar = tk.StringVar()
        self.tags_textvar.set(" ".join(project.metadata.Tags))
        entry_tags = tk.Entry(song_and_map_metadata_info_frame, textvariable=self.tags_textvar)
        entry_tags.grid(row=7, column=1, sticky="EW")

        # callback
        self.artist_textvar.trace_add("write", callback=lambda name, index, mode,
                                                               sv=self.artist_textvar: self.on_update_callback(sv,
                                                                                                               self.romanised_artist_textvar))
        self.title_textvar.trace_add("write",
                                     callback=lambda name, index, mode, sv=self.title_textvar: self.on_update_callback(
                                         sv, self.romanised_title_textvar))

        for widget in song_and_map_metadata_info_frame.winfo_children():
            widget.grid_configure(pady=2, padx=5)

    def on_update_callback(self, from_stringvar: tk.StringVar, to_stringvar: tk.StringVar):
        to_stringvar.set(from_stringvar.get())


class TabDifficulty(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        difficulty_info_frame = tk.LabelFrame(self, text="Difficulty")
        difficulty_info_frame.grid(row=0, column=0, padx=20, pady=20)

        # hp drain rate
        label_hp_drain_rate = tk.Label(difficulty_info_frame, text="HP Drain Rate")
        label_hp_drain_rate.grid(row=0, column=0, sticky="W")
        self.hp_drain_rate = tk.DoubleVar()
        self.hp_drain_rate.set(4.5)
        scale_hp_drain_rate = tk.Scale(difficulty_info_frame, from_=0, to=10, variable=self.hp_drain_rate,
                                       orient="horizontal", resolution=0.1, length=150)
        scale_hp_drain_rate.grid(row=0, column=1)
        label_hp_drain_rate_doc = tk.Label(difficulty_info_frame,
                                           text="The constant rate of health-bar drain throughout the song")
        label_hp_drain_rate_doc.grid(row=1, column=0, columnspan=2, sticky="W")

        # circle size
        label_circle_size = tk.Label(difficulty_info_frame, text="Circle Size")
        label_circle_size.grid(row=2, column=0, sticky="W")
        self.circle_size = tk.DoubleVar()
        self.circle_size.set(4)
        scale_circle_size = tk.Scale(difficulty_info_frame, from_=2, to=7, variable=self.circle_size,
                                     orient="horizontal", resolution=0.1, length=150)
        scale_circle_size.grid(row=2, column=1)
        label_circle_size_doc = tk.Label(difficulty_info_frame,
                                         text="The radial size of hit circles and sliders")
        label_circle_size_doc.grid(row=3, column=0, columnspan=2, sticky="W")

        # Approach rate
        label_approach_rate = tk.Label(difficulty_info_frame, text="Approach rate")
        label_approach_rate.grid(row=4, column=0, sticky="W")
        self.approach_rate = tk.DoubleVar()
        self.approach_rate.set(4)
        scale_approach_rate = tk.Scale(difficulty_info_frame, from_=0, to=10, variable=self.approach_rate,
                                       orient="horizontal", resolution=0.1, length=150)
        scale_approach_rate.grid(row=4, column=1)
        label_approach_rate_doc = tk.Label(difficulty_info_frame,
                                           text="The speed at which the objects will appear")
        label_approach_rate_doc.grid(row=5, column=0, columnspan=2, sticky="W")

        # overall difficulty
        label_overall_difficulty = tk.Label(difficulty_info_frame, text="Overall Difficulty")
        label_overall_difficulty.grid(row=6, column=0, sticky="W")
        self.overall_difficulty = tk.DoubleVar()
        self.overall_difficulty.set(4)
        scale_overall_difficulty = tk.Scale(difficulty_info_frame, from_=0, to=10, variable=self.overall_difficulty,
                                            orient="horizontal", resolution=0.1, length=150)
        scale_overall_difficulty.grid(row=6, column=1)
        label_overall_difficulty_doc = tk.Label(difficulty_info_frame,
                                                text="The harshness of the hit window and the difficulty of spinners")
        label_overall_difficulty_doc.grid(row=7, column=0, columnspan=2, sticky="W")


class BeatmapConfig(tk.Frame):

    def __init__(self, parent, project):
        tk.Frame.__init__(self, parent)

        notebook = ttk.Notebook(self)

        self.tab_general = TabGeneral(notebook, project)
        self.tab_difficulty = TabDifficulty(notebook)
        self.tab_audio = TabDifficulty(notebook)
        self.tab_colours = TabDifficulty(notebook)
        self.tab_design = TabDifficulty(notebook)
        self.tab_advanced = TabDifficulty(notebook)

        notebook.add(self.tab_general, text="General")
        notebook.add(self.tab_difficulty, text="Difficulty")
        notebook.add(self.tab_audio, text="Audio")
        notebook.add(self.tab_colours, text="Colors")
        notebook.add(self.tab_design, text="Design")
        notebook.add(self.tab_advanced, text="Advances")

        notebook.pack(padx=5, pady=5, fill="both")
