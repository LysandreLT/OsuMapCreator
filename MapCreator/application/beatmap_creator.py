# application for creating beatmap from input audio
import os.path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

from tkinterdnd2 import DND_FILES, TkinterDnD

from MapCreator.Utils import utils
from MapCreator.Utils.beatmapset import BeatmapSet

from MapCreator.application.configuration import BeatmapConfig


class tkinterApp(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.resizable(False, False)
        self.title('App')
        self.geometry('900x512')

        # init menu
        self.create_menu_bar()

        self._frame = None
        self.switch_frame(Project)

        # frame.grid(row=0, column=0, sticky="nsew")

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(fill=tk.BOTH)

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        # file
        menu_file = tk.Menu(menu_bar, tearoff=0)

        # menu_file.add_separator()
        #
        # menu_file.add_command(label="Test", command=lambda: self.switch_frame(ModelTest))
        # menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        self.config(menu=menu_bar)


class Project(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # frame
        _frame = tk.Frame(self, width=master.winfo_width(), height=master.winfo_height())
        _frame.pack()

        frame_music = tk.Frame(_frame)
        frame_music.grid(row=0, column=0)

        # DND
        dnd_frame = tk.Frame(frame_music)
        dnd_frame.pack()

        dnd_image_tk = tk.PhotoImage(file="./ressources/dnd.gif")
        label_dnd = tk.Label(dnd_frame, text="Drag and drop mp3 file here", image=dnd_image_tk)
        label_dnd.image = dnd_image_tk
        label_dnd.pack()
        label_dnd.drop_target_register(DND_FILES)
        label_dnd.dnd_bind("<<Drop>>", self.drop_inside_image)

        btn_browse = tk.Button(frame_music, text="Browse file", command=self.browse_file)
        btn_browse.pack()
        tk.Button(frame_music, text="Generate", command=self.generate_beatmap).pack()

        self.audio_path = tk.StringVar()
        label = tk.Label(self, textvariable=self.audio_path, fg="#FF0000", font="Verdana 10 underline")
        label.pack()

        self.config = BeatmapConfig(_frame)
        self.config.grid(row=0, rowspan=3, column=1, sticky="EW")

    def drop_inside_image(self, event):
        file_path = self.parse_drop_files(event.data)
        if file_path is not None:
            if list(filter(file_path.endswith, [".ogg", ".mp3", ".wav"])) != []:
                self.audio_path.set(file_path)
            else:
                messagebox.showerror('File Error', 'Error: Not an audio file!')

    def parse_drop_files(self, filename):
        size = len(filename)
        res = []
        name = ""
        idx = 0
        while idx < size:
            if filename[idx] == "{":
                j = idx + 1
                while filename[j] != "}":
                    name += filename[j]
                    j += 1
                res.append(name)
                name = ""
                idx = j
            elif filename[idx] == " " and name != "":
                res.append(name)
                name = ""
            elif filename[idx] != " ":
                name += filename[idx]
            idx += 1
        if name != "":
            res.append(name)
        if len(res) != 1:
            messagebox.showerror('File Error', 'Error: More than one file dropped!')
        else:
            return res[0]

    def generate_beatmap(self):
        directory = self.browse_folder()
        if directory != "":
            print("generating beatmap!")

            beatmap = BeatmapSet()

            title = self.config.tab_general.title.get()
            if title == "":
                return -1
            title_unicode = self.config.tab_general.romanised_title.get()
            if title_unicode == "":
                return -1
            artist = self.config.tab_general.artist.get()
            if artist == "":
                return -1
            artist_unicode = self.config.tab_general.romanised_artist.get()
            if artist_unicode == "":
                return -1
            creator = self.config.tab_general.beatmap_creator.get()
            if creator == "":
                return -1
            version = self.config.tab_general.difficulty.get()
            if version == "":
                return -1
            source = self.config.tab_general.source.get()
            if source == "":
                source = " "
            tags = self.config.tab_general.tags.get()
            if tags == "":
                return -1

            dir_path = os.path.join(directory, f"{artist} - {title}")

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            shutil.copyfile(self.audio_path.get(), os.path.join(dir_path, "audio.mp3"))

            beatmap.file_name = os.path.join(dir_path, f"{artist} - {title} ({creator}) [{version}].osu")

            beatmap.file_format = "osu file format v14\n\n"
            beatmap.write_append(beatmap.file_name, beatmap.file_format, 'w')

            beatmap.build_general(AudioFilename="audio.mp3")
            beatmap.build_editor()
            beatmap.build_metadata(Title=title, TitleUnicode=title_unicode, Artist=artist, ArtistUnicode=artist,
                                   Creator=creator, Version=version, Source=source, Tags=tags)
            beatmap.build_difficulty(HPDrainRate=self.config.tab_difficulty.hp_drain_rate.get(),
                                     CircleSize=self.config.tab_difficulty.circle_size.get(),
                                     OverallDifficulty=self.config.tab_difficulty.overall_difficulty.get(),
                                     ApproachRate=self.config.tab_difficulty.approach_rate.get())
            beatmap.build_events()
            beatmap.build_hitobjects_and_timingpoints(os.path.join(dir_path, "audio.mp3"),
                                                      1 / beatmap.difficulty.OverallDifficulty)

            utils.write_osz_archive(dir_path, dir_path)
            utils.delete_tree(dir_path)
            messagebox.showinfo("Beatmap created!", f"beatmap created in {os.path.dirname(dir_path)}")

            utils.explore(os.path.dirname(dir_path))

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="",
                                              title="Select a File")
        self.audio_path.set(filename.strip())

    def browse_folder(self):
        return filedialog.askdirectory(initialdir="",
                                       title="Select a Folder")


if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()
