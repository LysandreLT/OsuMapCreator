import datetime
import json
import time
from tkinter.messagebox import askyesno
from tkinter import filedialog
import tkinter as tk
import os

import MapCreator.Utils.utils as util


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # dest Dir
        self.location = os.getcwd()

        # configure the root window
        self.title('App')
        self.geometry('480x360')

        # init menu
        self.create_menu_bar()

        # Location frame
        frame_output = tk.Frame(self)
        frame_output.pack(fill=tk.X)

        label_output = tk.Label(frame_output, text="Output :")
        label_output.pack(side=tk.LEFT, padx=5)

        location_frame = tk.Frame(self)
        location_frame.pack(fill=tk.X, padx=5)

        lbl1_location = tk.Label(location_frame, text=" Location :", width=6)
        lbl1_location.pack(side=tk.LEFT, padx=5, pady=5)

        self.entry_location_output = tk.Entry(location_frame)
        self.entry_location_output.pack(fill=tk.X, padx=5, expand=True)
        self.entry_location_output.insert(0, self.location)

        # Data frame
        frame_data = tk.Frame(self)
        frame_data.pack(fill=tk.X)

        label_data = tk.Label(frame_data, text="Archives or Folder path:")
        label_data.pack(side=tk.LEFT, padx=5)

        frame_data_location = tk.Frame(self)
        frame_data_location.pack(fill=tk.X, padx=5)

        lbl1_location = tk.Label(frame_data_location, text=" Location :", width=6)
        lbl1_location.pack(side=tk.LEFT, padx=5, pady=5)

        self.entry_location_data = tk.Entry(frame_data_location)
        self.entry_location_data.pack(fill=tk.X, padx=5, expand=True)

        # delete original
        frame_delete_origin = tk.Frame(self)
        frame_delete_origin.pack(fill=tk.X)

        label_delete_origin = tk.Label(frame_delete_origin, text="Delete 'Archives or Folder path' after extraction?")
        label_delete_origin.pack(side=tk.LEFT, padx=5)

        self.is_delete_origin_data = tk.BooleanVar()
        ChkBttn_delete_origin = tk.Checkbutton(frame_delete_origin, width=15, variable=self.is_delete_origin_data,
                                               command=lambda: self.confirm(
                                                   f"Are you sure you want to delete {self.entry_location_output.get()}?"))
        ChkBttn_delete_origin.pack(side=tk.LEFT, padx=5, pady=5)

        # btn
        frame = tk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.BOTH, expand=True)

        extract_btn = tk.Button(self, text="Extract", command=self.extract_all)
        extract_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        extract_btn = tk.Button(self, text="Debug", command=self.debug)
        extract_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)
        menu_file = tk.Menu(menu_bar, tearoff=0)
        menu_file.add_command(label="Change Location", command=lambda: self.browse_folder(self.entry_location_output))
        menu_file.add_command(label="Import Archive", command=lambda: self.browse_file(self.entry_location_data))
        menu_file.add_command(label="Import Archives", command=lambda: self.browse_folder(self.entry_location_data))
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=menu_file)

        self.config(menu=menu_bar)

    def browse_file(self, entry: tk.Entry):
        filename = filedialog.askopenfilename(initialdir=self.location,
                                              title="Select a File",
                                              filetypes=(("all files", "*.*"), ("Text files", "*.txt*")))
        entry.delete(0, tk.END)
        entry.insert(0, filename)

    def browse_folder(self, entry: tk.Entry):
        self.location = filedialog.askdirectory(initialdir=self.location,
                                                title="Select a Folder")
        entry.delete(0, tk.END)
        entry.insert(0, self.location)

    def extract_all(self) -> None:
        start = time.time_ns()
        if not len(self.entry_location_data.get()) == 0:
            # check if all folder exist
            if not os.path.exists(self.entry_location_output.get()):
                os.makedirs(self.entry_location_output.get() + "/maps")
            # check if folder + 'maps' exist
            if not os.path.exists(self.entry_location_output.get() + "/maps"):
                os.mkdir(self.entry_location_output.get() + "/maps")

            # check if data is folder else is file
            if os.path.isdir(self.entry_location_data.get()):
                util.clean_archive_folder(self.entry_location_data.get(), self.entry_location_output.get())
                print("done!")
            else:
                util.clean_archive(self.entry_location_data.get(), self.entry_location_output.get())
        else:
            print("no path")

        if os.path.exists(os.path.join(self.entry_location_output.get(), "temp")):
            util.delete_tree(os.path.join(self.entry_location_output.get(), "temp"))
        if self.is_delete_origin_data.get():
            if os.path.exists(self.entry_location_data.get()):
                util.delete_tree(self.entry_location_data.get())
        end = time.time_ns()
        time_in_sec = (end - start) / 1000000000
        print(f"done in {time_in_sec}s")

    def debug(self):
        print("is dir : ", os.path.isdir(self.entry_location_data.get()))
        print(self.is_delete_origin_data.get())
        # print(str(datetime.timedelta(seconds=util.get_duration("C:/Users/hugob/dev/python/OSU_AI/MapCreator/app/ui/maps/1953850 RIOT - Overkill/drum-hitclap.ogg"))))
        beatmap = util.parse("C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/app/ui/maps/1953850 RIOT - Overkill/RIOT - Overkill (Hareimu) [KILL THEM ALL].osu")
        # json.dumps(beatmap)
        # parsed = json.loads()
        # print(json.dumps(parsed, indent=4))
        util.write(beatmap,"C:/Users/hugob/dev/python/OsuMapCreator/MapCreator/app/ui/maps","test",util.Type.JSON)

    def confirm(self, message: str):
        if self.is_delete_origin_data.get():
            answer = askyesno(title="confirmation", message=message)
            if not answer:
                self.is_delete_origin_data.set(False)


if __name__ == "__main__":
    app = App()
    # Let the window wait for any events
    app.mainloop()
