# application for creating beatmap from input audio
import os
import tkinter as tk
from tkinter import ttk, filedialog,scrolledtext

LARGEFONT = ("Verdana", 35)


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('App')
        self.geometry('480x360')

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
        for F in (ModelTest, ProjectPresentation):
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
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Presentation", command=lambda: self.show_frame(ProjectPresentation))
        menu_file.add_command(label="Test", command=lambda: self.show_frame(ModelTest))

        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        self.config(menu=menu_bar)


# first window frame startpage
# class StartPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#
#         # label of frame Layout 2
#         label = ttk.Label(self, text="Startpage", font=LARGEFONT)
#
#         # putting the grid in its place by using
#         # grid
#         label.grid(row=0, column=4, padx=10, pady=10)
#
#         button1 = ttk.Button(self, text="Page 1",
#                              command=lambda: controller.show_frame(ModelTest))
#
#         # putting the button in its place by
#         # using grid
#         button1.grid(row=1, column=1, padx=10, pady=10)

class ProjectPresentation(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Presentation", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)


insert_text = """Model de test :
beatmap réalisé a partir des onsets d'une piste audio
les position x et y sont aléatoire.
modèle peut précis ne prenant pas en compte la difficultés.
#proof of concept
"""
class ModelTest(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Model test")
        label.grid(row=0, column=2, padx=10, pady=10)

        # audio path
        location = ""

        # Audio frame
        label_audio = tk.Label(self, text=" Audio :", width=6)
        label_audio.grid(row=1, column=0, padx=5, pady=5)
        self.s = tk.StringVar()
        entry_audio = tk.Entry(self, textvariable=self.s, width=55)
        entry_audio.grid(row=1, column=1, columnspan=3, sticky=tk.W + tk.E)
        entry_audio.insert(0, self.location)
        self.s.set(location)
        btn_browse = tk.Button(self, text="Browse audio", command=self.browse_file)
        btn_browse.grid(row=1, column=4, sticky=tk.W + tk.E)

        # description
        label_description = tk.Label(self, text="Description")
        label_description.grid(row=2, column=0)

        text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                                 width=40, height=8)

        text_area.grid(column=0, row=3, columnspan=5, sticky=tk.W + tk.E)
        text_area.insert(tk.END, insert_text)
        text_area.config(state = tk.DISABLED)

        # project repo path entry?
        # create project folder?
        # new project?
        # existing project?


        # btn
        btn_create = tk.Button(self, text="Create beatmap set", command=self.create)
        btn_create.grid(row=4, column=0, columnspan=2, sticky=tk.W + tk.E)

    def browse_file(self):
        filename = filedialog.askopenfilename(initialdir="",
                                              title="Select a File",
                                              filetypes=(("all files", "*.*"), ("Text files", "*.txt*")))
        self.s.set(filename)

    def create(self):

        pass


if __name__ == "__main__":
    app = tkinterApp()
    app.mainloop()
