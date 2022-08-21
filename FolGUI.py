import tkinter as tk
from tkinter import ttk

from tkinter import filedialog

import os
import shutil
import sys


class LabelInput(tk.Frame):
    def __init__(
        self,
        parent,
        label="",
        input_class=ttk.Entry,
        input_var=None,
        input_args=None,
        label_args=None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["text"] = label
            input_args["variable"] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
            input_args["textvariable"] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get("1.0", tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            return ""

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input) in (ttk.Checkbutton, ttk.Radiobutton):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete("1.0", tk.END)
            self.input.insert("1.0", value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


class FolderInfo(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.inputs = {}
        extensions = self.get_extensions()

        folderinfo = tk.LabelFrame(self, text="Folder Info")

        self.inputs["folder"] = LabelInput(
            folderinfo, "Folder path", input_var=tk.StringVar(), input_class=ttk.Entry
        )
        self.inputs["folder"].grid(row=0, column=0)

        self.inputs["get_path"] = tk.Button(
            self, text="Folder to Organize", command=self.get_folder, bg="gray"
        )
        self.inputs["get_path"].grid(row=1, column=0, pady=3, sticky=tk.W)

        self.inputs["extensions"] = LabelInput(
            folderinfo,
            "File Extension",
            input_class=ttk.Combobox,
            input_var=tk.StringVar(),
            input_args={"values": list(extensions)},
        )
        self.inputs["extensions"].grid(row=0, column=1)

        folderinfo.grid(row=0, column=0, sticky=tk.W + tk.E)

    def get_folder(self):
        folderpath = filedialog.askdirectory()
        self.inputs["folder"].set(folderpath)

    def get_extensions(self):
        file_extensions = set()
        listoffiles = [f for f in os.listdir(".") if os.path.isfile(f)]
        for wo in listoffiles:
            if wo not in file_extensions:
                file_extensions.add(os.path.splitext(wo)[-1])
        return file_extensions

    def get(self):
        data = {}
        for key, widget in self.inputs.items():
            if type(widget) != tk.Button:
                data[key] = widget.get()
        return data

    def reset(self):
        for widget in self.inputs.values():
            widget.set("")


class FileApp(tk.Tk):
    """Root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ttk.Label(
            self, text="FileOrganizerLite", font=("TKDefaultFont", 12, "bold")
        ).grid(row=0)

        self.folderwidget = FolderInfo(self)
        self.folderwidget.grid(row=2, padx=10)

        self.organizebtn = tk.Button(
            self, text="Organize", command=self.on_organize, bg="gray"
        )
        self.organizebtn.grid(sticky=tk.E + tk.S, row=2, column=1, pady=3, padx=5)

    def on_organize(self):
        info = self.folderwidget.get()
        location = os.listdir(f"/{info['extensions']}_files")
        directory_path = os.path.join(info['folder'] + location)
        for filename in info['folder']:
            if not filename.endswith(info['extensions']):
                continue
            else:
                shutil.move('' + filename, directory_path)

if __name__ == "__main__":
    app = FileApp()
    app.mainloop()
