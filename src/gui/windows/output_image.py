import tkinter as tk
from PIL import ImageTk, Image


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

        self.img_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    def _add_menubar(self):
        self.menubar = tk.Menu(self.master)

        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label="Save Image")
        file.add_separator()
        file.add_command(label="Close Window")

        edit = tk.Menu(self.menubar, tearoff=0)
        edit.add_command(label="Undo")
        edit.add_command(label="Clear All")

        help = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="File", menu=file)
        self.menubar.add_cascade(label="Edit", menu=edit)
        self.menubar.add_cascade(label="Help", menu=help)

        self.master.config(menu=self.menubar)

    def _add_widgets(self):
        self._add_menubar()
        self._add_image()

    def _close_window(self):
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
            self._close_window()
            self._new_window()


if __name__ == '__main__':
    root = tk.Tk()
    op_img_screen = OutputImageWindow(root)
    btn = tk.Button(root, text="open", command=op_img_screen.open_window).pack()
    root.mainloop()
