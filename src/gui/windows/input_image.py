import tkinter as tk
import tkinter.ttk as ttk

from PIL import ImageTk, Image

from src.gui.constants import *


class InputImageWindow:
    def __init__(self, parent):
        self.master = None
        self.parent = parent

    def _add_image(self):
        self.img_frame = tk.LabelFrame(self.master, text='Image', padx=5, pady=5)

        global img
        img = ImageTk.PhotoImage(Image.open(self.filename))
        img_label = tk.Label(self.img_frame, image=img)
        img_label.pack()

        self.img_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    def _add_controls(self):
        self.controls_frame = tk.LabelFrame(self.master, text='Controls', padx=5, pady=5)
        self.controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

        color_label = tk.Label(self.controls_frame, bg='#000000', height=3)

        r_label = tk.Label(self.controls_frame, text='R')
        g_label = tk.Label(self.controls_frame, text='G')
        b_label = tk.Label(self.controls_frame, text='B')
        r_spinbox = tk.Spinbox(self.controls_frame, width=4, from_=0, to=255, wrap=True)
        g_spinbox = tk.Spinbox(self.controls_frame, width=4, from_=0, to=255, wrap=True)
        b_spinbox = tk.Spinbox(self.controls_frame, width=4, from_=0, to=255, wrap=True)

        common_colors_label = tk.Label(self.controls_frame, text='Common Colors', wraplength=100, justify=tk.LEFT)
        common_colors_combobox = ttk.Combobox(self.controls_frame, width=10)
        common_colors_combobox['values'] = COMMON_COLORS

        brush_size_label = tk.Label(self.controls_frame, text='Brush Size', wraplength=100, justify=tk.LEFT)
        brush_size_spinbox = tk.Spinbox(self.controls_frame, width=3, from_=1, to=15, wrap=True)

        color_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)
        r_label.grid(row=1, column=0, padx=5, pady=5)
        g_label.grid(row=2, column=0, padx=5, pady=5)
        b_label.grid(row=3, column=0, padx=5, pady=5)
        r_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        g_spinbox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        b_spinbox.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        common_colors_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        common_colors_combobox.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        brush_size_label.grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        brush_size_spinbox.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)

    def _add_menubar(self):
        self.menubar = tk.Menu(self.master)

        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label="New Image")
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
        self._add_controls()

    def _close_window(self):
        self.master.destroy()

    def _new_window(self):
        self.master = tk.Toplevel()
        self.master.title('Input Image')
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
    ip_img_screen = InputImageWindow(root)
    btn = tk.Button(root, text="open", command=ip_img_screen.open_window).pack()
    root.mainloop()
