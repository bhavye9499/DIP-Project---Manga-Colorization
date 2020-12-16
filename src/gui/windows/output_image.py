import tkinter as tk
from PIL import ImageTk, Image

from src.gui.commands.output_image_cmds import *


class OutputImageWindow:
    def __init__(self, parent):
        self.filename = None
        self.master = None
        self.parent = parent

    def _add_image(self):
        self.img_frame = tk.LabelFrame(self.master, text='Image', padx=5, pady=5)

        global img
        img = ImageTk.PhotoImage(Image.open(self.filename))
        img_label = tk.Label(self.img_frame, image=img)
        img_label.pack()

        globals.curr_output_img = Image.open(self.filename).convert('RGB')

        self.img_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    def _add_menubar(self):
        self.menubar = tk.Menu(self.master)

        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label="Save Image      Ctrl+S", command=file_save_image_command)
        file.add_separator()
        file.add_command(label="Close Window    Ctrl+W", command=self.close_window)

        edit = tk.Menu(self.menubar, tearoff=0)
        edit.add_command(label="Undo         Ctrl+Z", command=edit_undo_command)
        edit.add_command(label="Clear All    Ctrl+X", command=edit_clear_all_command)

        help = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="File", menu=file)
        self.menubar.add_cascade(label="Edit", menu=edit)
        self.menubar.add_cascade(label="Help", menu=help)

        self.master.config(menu=self.menubar)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-s>', file_save_image_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-w>', file_close_window_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-z>', edit_undo_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-x>', edit_clear_all_key_command)

    def _add_widgets(self):
        self._add_menubar()
        self._add_image()

    def close_window(self):
        self.master.destroy()

    def _new_window(self):
        self.master = tk.Toplevel()
        self.master.title('Output Image')
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        self._add_widgets()

    def open_window(self, filename):
        self.filename = filename
        if self.master is None:
            self._new_window()
        else:
            self.close_window()
            self._new_window()


if __name__ == '__main__':
    root = tk.Tk()
    op_img_screen = OutputImageWindow(root)
    btn = tk.Button(root, text="open", command=op_img_screen.open_window).pack()
    root.mainloop()
