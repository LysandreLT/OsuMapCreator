# application for creating beatmap from input audio
import os.path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from typing import List

import mutagen
from tkinterdnd2 import DND_FILES, TkinterDnD

from MapCreator.Utils.beatmapset import BeatmapSet
from MapCreator.Utils.models.models import General, TimingPoint, Event, Difficulty, Metadata, Editor, ColourSection, \
    HitObject
from MapCreator.Utils.parser import Parse
from MapCreator.application.configuration import BeatmapConfig
from MapCreator.application.model import ModelTest, ProjectPresentation


class tkinterApp(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.resizable(False, False)
        self.title('App')
        self.geometry('1080x720')

        self.current_project_dir = ""

        # init menu
        self.create_menu_bar()

        self._frame = None
        self.switch_frame(ProjectPresentation)

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
        menu_file.add_command(label="New project", command=lambda: self.switch_frame(NewProject))
        menu_file.add_command(label="Open project", command=self.browse_folder)
        # menu_file.add_separator()
        # menu_file.add_command(label="Beatmap configuration", command=lambda: self.switch_frame(BeatmapConfigtk))
        menu_file.add_separator()
        menu_file.add_command(label="Presentation", command=lambda: self.switch_frame(ProjectPresentation))
        menu_file.add_command(label="Test", command=lambda: self.switch_frame(ModelTest))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)
        # edit
        # menu_edit = tk.Menu(menu_bar, tearoff=0)
        # menu_edit.add_command(label="Beatmap configuration", command=lambda: self.switch_frame(BeatmapConfig))
        # menu_edit.add_separator()
        # menu_edit.add_command(label="Volume")
        # menu_edit.add_command(label="slider speed")
        # menu_bar.add_cascade(label="Edit", menu=menu_edit)

        self.config(menu=menu_bar)

    def import_map(self):
        # TODO possibility to import an existing osu map / extract and parse
        pass

    def browse_folder(self):
        filename = filedialog.askdirectory(initialdir="",
                                           title="Select a Folder")
        self.current_project_dir = filename
        if filename != "":
            self.switch_frame(Project)


class NewProject(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.artist = ""
        self.title = ""

        # location
        location_frame = tk.Frame(self)
        location_frame.pack(fill=tk.X)

        lbl1_location = tk.Label(location_frame, text=" Location :", width=6)
        lbl1_location.pack(side=tk.LEFT, padx=5, pady=5)

        btn_browse_location = tk.Button(location_frame, text="Select File",
                                        command=self.browse_folder)
        btn_browse_location.pack(side=tk.RIGHT, padx=5, pady=5)

        self.location = tk.StringVar()
        entry_location = tk.Entry(location_frame, textvariable=self.location)
        entry_location.pack(fill=tk.X, padx=5, expand=True)

        # create new
        create_new_local_dir_frame = tk.Frame(self)
        create_new_local_dir_frame.pack(fill=tk.X)

        self.isChecked = tk.BooleanVar()
        checkbox = tk.Checkbutton(create_new_local_dir_frame, text="Create a local directory for projects ?",
                                  variable=self.isChecked)
        checkbox.pack(side=tk.LEFT, pady=5)
        # DND
        dnd_frame = tk.Frame(self)
        dnd_frame.pack(fill=tk.X)

        dnd_image_tk = tk.PhotoImage(file="./ressources/dnd.gif")
        label_dnd = tk.Label(dnd_frame, text="Drag and drop mp3 file here", image=dnd_image_tk)
        label_dnd.image = dnd_image_tk
        label_dnd.pack()
        label_dnd.drop_target_register(DND_FILES)
        label_dnd.dnd_bind("<<Drop>>", self.drop_inside_image)

        btn_browse = tk.Button(self, text="Browse file", command=self.browse_file)
        btn_browse.pack()

        self.audio_path = tk.StringVar()
        label = tk.Label(self, textvariable=self.audio_path, fg="#FF0000", font="Verdana 10 underline")
        label.pack()

        # btn
        # frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        # frame.pack(fill=tk.BOTH, expand=True)
        frame = tk.Frame(self)
        frame.pack(fill=tk.X)

        btn_create_project = tk.Button(frame, text="Create", command=lambda: self.create(master))
        btn_create_project.pack(side=tk.RIGHT, padx=10, pady=5, ipadx=5, ipady=5)

        btn_cancel = tk.Button(frame, text="Cancel", command=lambda: self.cancel(master))
        btn_cancel.pack(side=tk.RIGHT, padx=10, pady=5, ipadx=5, ipady=5)

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

    def browse_folder(self):
        filename = filedialog.askdirectory(initialdir="",
                                           title="Select a Folder")
        self.location.set(filename.strip())

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="",
                                              title="Select a File")
        self.audio_path.set(filename.strip())

    def cancel(self, master):
        self.location.set("")
        master.switch_frame(ProjectPresentation)

    def create(self, master):
        if self.location.get() and os.path.exists(self.location.get()):
            if self.audio_path.get() and os.path.exists(self.audio_path.get()):
                if self.isChecked.get():
                    if not os.path.exists(os.path.join(self.location.get(), "songs")) and os.path.basename(
                            self.location.get()) != "songs":
                        os.mkdir(os.path.join(self.location.get(), "songs"))
                    if os.path.basename(self.location.get()) != "songs":
                        self.create_project(os.path.join(self.location.get(), "songs"), master)
                    else:
                        self.create_project(self.location.get(), master)
                else:
                    self.create_project(self.location.get(), master)
            else:
                messagebox.showerror('Missing indormations', 'Error: Please select an audio file')
        else:
            messagebox.showerror('Missing indormations', 'Error: Please enter a valid location path for your project')

    def create_project(self, project_path, master):
        # TODO don't like to set the artist like this here. may be if no meta detected, go to project and wait for user
        #  to input artist and title and save to create the project repo
        # TODO find a way to keep the audio path and move it late to the project repo
        # reset artist and title
        artist = ""
        title = ""
        # Search audio metadata
        try:
            file = mutagen.File(self.audio_path.get())
            try:
                artist = file["artist"]
                title = file["title"]
            except:
                title = file["TIT2"]
                artist = file["TPE1"]
        except:
            answer = MyDialog(self)
            if answer.result[0] is not None:
                artist = answer.result[0]
            if answer.result[1] is not None:
                title = answer.result[1]

        # create project dir
        project_dir = os.path.join(project_path, f"{artist} - {title}")
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        # opening the project interface
        master.current_project_dir = project_dir
        shutil.move(src=self.audio_path.get(), dst=project_dir)
        os.rename(os.path.join(project_dir, os.path.basename(self.audio_path.get())),
                  os.path.join(project_dir, "audio.mp3"))
        master.switch_frame(Project)


class MyDialog(tk.simpledialog.Dialog):

    def body(self, master):
        tk.Label(master, text="Please enter the name of the artist:").grid(row=0)
        tk.Label(master, text="Please enter the name of the song:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e1.insert(0, "")
        self.e2.insert(0, "")
        return self.e1  # initial focus

    def buttonbox(self):
        box = tk.Frame(self)
        tk.Button(box, text="Validate", width=10, command=self.ok, default=tk.ACTIVE) \
            .pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(box, text="Cancel", width=10, command=self.cancel) \
            .pack(side=tk.LEFT, padx=5, pady=5)
        box.pack()

    def apply(self):
        artist = self.e1.get()
        title = self.e2.get()
        self.result = artist, title

    def validate(self):
        if self.e1.get() != "" and self.e2.get() != "":
            self.apply()
            return True
        messagebox.showinfo("infos", "please fill every fields!")
        return False


class Project(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # frame
        _frame = tk.Frame(self, width=master.winfo_width(), height=master.winfo_height())
        _frame.pack()

        self.listbox = tk.Listbox(_frame, selectmode=tk.SINGLE, background="#ffe0d6")
        self.listbox.place(relheight=1, relwidth=0.25)
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        self.listbox.bind("<<ListboxSelect>>", lambda event: self.refresh_list_box(event, master))
        self.refresh_list_box(None, master)

        # Parser
        self.parser: Parse = None
        self.general: General = None
        self.editor: Editor = None
        self.metadata: Metadata = None
        self.difficulty: Difficulty = None
        # self.events:Event = None
        self.timing_points: List[TimingPoint] = None
        # self.colours:ColourSection = None
        self.hit_objects: List[HitObject] = None

        # TODO here we take the first beatmap in the project folder --> to change
        for file in set(self.listbox.get(0, "end")):
            self.initialize_parsing(master, file)
            break

        # self.initialize_config()

        # config
        frame_config = tk.Frame(_frame)
        frame_config.place(relx=0.25)

        self.config = BeatmapConfig(frame_config, self)
        self.config.pack(side=tk.LEFT)

        # btn
        tk.Button(frame_config, text="Save", command=self.save).pack()
        tk.Button(frame_config, text="Generate").pack()
        tk.Button(frame_config, text="Export").pack()

        # frame = tk.Frame(master,background="#ff0000")
        # frame.place(relx=0.25,y=350, relwidth=0.75, relheight=1.00)
        # TODO add logs and configs file to remember if already have a work dir and a proj dir
        # TODO detect if .osu (and music) in current project --> if have, parse --> else propose if they want to create a new project/or wait for them to save and create a repo
        # TODO set / initialize config panels with the parsed values
        # TODO add and finish all configs panels
        # TODO add save btn to save modif --> rewrite all file?(utils/beatmapset)
        # TODO add beatmap creation btn

    def initialize_parsing(self, master, file: str):
        if file.endswith(".osu"):
            # create a new parser each time we parse a map? should be a singleton or something similar
            self.parser = Parse()
            self.parser.parse_file(os.path.join(master.current_project_dir, file))
            self.initialize_config()

    def initialize_config(self):
        if self.parser is not None:
            self.general = self.parser.general
            self.editor = self.parser.editor
            self.metadata = self.parser.metadata
            self.difficulty = self.parser.difficulty
            self.timing_points = self.parser.timing_points
            self.hit_objects = self.parser.hit_objects
            print(self.general.__dict__)

    def drop_inside_list_box(self, event):
        self.listbox.insert("end", event.data)

    def refresh_list_box(self, event, master):
        indices = self.listbox.curselection()
        if indices:
            file = self.listbox.get(indices[0])
            self.initialize_parsing(master, file)
        # TODO check if any change before refreshing
        self.listbox.delete(0, "end")
        if os.path.exists(master.current_project_dir):
            for file in os.listdir(master.current_project_dir):
                if file not in set(self.listbox.get(0, "end")):
                    self.listbox.insert("end", file)

    def fetch_metadata(self, beatmap):
        self.metadata.Artist = self.config.tab_general.artist_textvar.get()
        self.metadata.ArtistUnicode = self.config.tab_general.romanised_artist_textvar.get()
        self.metadata.Title = self.config.tab_general.title_textvar.get()
        self.metadata.TitleUnicode = self.config.tab_general.romanised_title_textvar.get()
        self.metadata.Creator = self.config.tab_general.creator_textvar.get()
        self.metadata.Version = self.config.tab_general.difficulty_textvar.get()
        self.metadata.Source = self.config.tab_general.source_textvar.get()
        self.metadata.Tags = self.config.tab_general.tags_textvar.get().split(" ")




    def fetch_config(self, beatmap):
        self.fetch_metadata(beatmap)

    def save(self):
        beatmap = BeatmapSet()
        self.fetch_config(beatmap)
        beatmap.build_general(**self.general.__dict__)
        beatmap.build_metadata(**self.metadata.__dict__)
        print(beatmap.metadata.Artist)

    def create(self):
        # TODO saving before creating (.osu)
        self.save()
        # TODO create --> method that process the audio in order to create the hit objects
        # TODO check if there is audio + .osu and .osu configured correctly
        #  --> zip everything
        pass

    def create_new_difficulty(self):
        # TODO create a custom difficulty for the map
        #  add it to the config so that the app remember
        pass

    def open_difficulty(self):
        # TODO a song can have many beatmaps of differents difficulty
        pass

    def export_map(self):
        # TODO export a choosen project
        pass

    def clear_all_notes(self):
        # TODO reset all hitpoints / hitobjects
        pass


if __name__ == "__main__":
    app = tkinterApp()
    # app.eval('tk::PlaceWindow . center')
    app.mainloop()
