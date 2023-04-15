# application for creating beatmap from input audio
import os.path
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

import mutagen
from tkinterdnd2 import DND_FILES, TkinterDnD

from MapCreator.application.configuration import BeatmapConfig
from MapCreator.application.model import ModelTest, ProjectPresentation


class tkinterApp(TkinterDnD.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.title('App')
        self.geometry('1080x720')

        self.current_project_dir = ""

        # init menu
        self.create_menu_bar()

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (ModelTest, ProjectPresentation, BeatmapConfig, NewProject, Project):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # default frame
        self.show_frame(ProjectPresentation)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        # file
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="New project", command=lambda: self.show_frame(NewProject))
        menu_file.add_command(label="Open project", command=self.browse_folder)
        # menu_file.add_separator()
        # menu_file.add_command(label="Beatmap configuration", command=lambda: self.show_frame(BeatmapConfigtk))
        menu_file.add_separator()
        menu_file.add_command(label="Presentation", command=lambda: self.show_frame(ProjectPresentation))
        menu_file.add_command(label="Test", command=lambda: self.show_frame(ModelTest))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)
        # edit
        # menu_edit = tk.Menu(menu_bar, tearoff=0)
        # menu_edit.add_command(label="Beatmap configuration", command=lambda: self.show_frame(BeatmapConfig))
        # menu_edit.add_separator()
        # menu_edit.add_command(label="Volume")
        # menu_edit.add_command(label="slider speed")
        # menu_bar.add_cascade(label="Edit", menu=menu_edit)

        self.config(menu=menu_bar)

    def browse_folder(self):
        filename = filedialog.askdirectory(initialdir="",
                                           title="Select a Folder")
        self.current_project_dir = filename
        (self.winfo_children())
        self.show_frame(Project)


class NewProject(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

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

        btn_create_project = tk.Button(frame, text="Create", command=lambda: self.create(controller))
        btn_create_project.pack(side=tk.RIGHT, padx=10, pady=5, ipadx=5, ipady=5)

        btn_cancel = tk.Button(frame, text="Cancel", command=lambda: self.cancel(controller))
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

    def cancel(self, controller):
        self.location.set("")
        controller.show_frame(ProjectPresentation)

    def create(self, controller):
        if self.location.get() and os.path.exists(self.location.get()):
            if self.audio_path.get() and os.path.exists(self.audio_path.get()):
                if self.isChecked.get():
                    if not os.path.exists(os.path.join(self.location.get(), "songs")) and os.path.basename(
                            self.location.get()) != "songs":
                        os.mkdir(os.path.join(self.location.get(), "songs"))
                    if os.path.basename(self.location.get()) != "songs":
                        self.create_project(os.path.join(self.location.get(), "songs"), controller)
                    else:
                        self.create_project(self.location.get(), controller)
                else:
                    self.create_project(self.location.get(), controller)
            else:
                messagebox.showerror('Missing indormations', 'Error: Please select an audio file')
        else:
            messagebox.showerror('Missing indormations', 'Error: Please enter a valid location path for your project')

    def create_project(self, project_path, controller):
        artist = ""
        title = ""
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

        project_dir = os.path.join(project_path, f"{artist} {title}")
        if not os.path.exists(project_dir):
            os.mkdir(project_dir)
        controller.current_project_dir = project_dir
        shutil.move(src=self.audio_path.get(), dst=project_dir)
        controller.show_frame(Project)


class MyDialog(tk.simpledialog.Dialog):

    def body(self, master):
        tk.Label(master, text="Please enter the name of the artist:").grid(row=0)
        tk.Label(master, text="Please enter the name of the song:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e1.insert(0,"")
        self.e2.insert(0, "")
        return self.e1  # initial focus

        # override buttonbox() to create your action buttons

    def buttonbox(self):
        box = tk.Frame(self)
        # note that self.ok() and self.cancel() are defined inside `Dialog` class
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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, background="#ffe0d6")
        self.listbox.place(relheight=1, relwidth=0.25)
        self.listbox.drop_target_register(DND_FILES)
        self.listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        self.listbox.bind("<Double-1>")  # TODO

        self.config = BeatmapConfig(self, None)
        self.config.place(relx=0.25, relwidth=0.75, relheight=0.95)

        tk.Button(self,text="test",command=lambda :self.refresh_curr_dir(controller)).pack()

        listbox_items = set(self.listbox.get(0,"end"))
        if os.path.exists(controller.current_project_dir):
            for file in os.listdir(controller.current_project_dir):
                self.listbox.insert("end",file)

    def drop_inside_list_box(self, event):
        self.listbox.insert("end", event.data)

    def refresh_curr_dir(self,controller):
        if os.path.exists(controller.current_project_dir):
            for file in os.listdir(controller.current_project_dir):
                if file not in set(self.listbox.get(0,"end")):
                    self.listbox.insert("end", file)


if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()
