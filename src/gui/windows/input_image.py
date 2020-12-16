import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image

from src.gui.commands.input_image_cmds import *
from src.globals.constants import *


class InputImageWindow:
    def __init__(self, parent):
        self.filename = None
        self.master = None
        self.parent = parent

    def _add_image(self):
        self.img_frame = tk.LabelFrame(self.master, text='Image', padx=5, pady=5)

        global img
        img = ImageTk.PhotoImage(Image.open(self.filename))
        self.img_label = tk.Label(self.img_frame, image=img)
        self.img_label.bind('<' + EVENT_LBUTTONDOWN + '>', brush_stroke_command)
        self.img_label.bind('<' + EVENT_MOUSEMOVE + '>', brush_stroke_command)
        self.img_label.bind('<' + EVENT_LBUTTONUP + '>', brush_stroke_command)
        self.img_label.pack()

        globals.raw_img = Image.open(self.filename).convert('L')
        globals.curr_scribbled_img = Image.open(self.filename).convert('RGB')

        self.img_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    def _add_controls(self):
        self.controls_frame = tk.LabelFrame(self.master, text='Controls', padx=5, pady=5)
        self.controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

        self.color_label = tk.Label(self.controls_frame, bg='#000000', height=3)

        r_label = tk.Label(self.controls_frame, text='R')
        g_label = tk.Label(self.controls_frame, text='G')
        b_label = tk.Label(self.controls_frame, text='B')
        tk_vars.r = tk.StringVar(self.controls_frame)
        tk_vars.g = tk.StringVar(self.controls_frame)
        tk_vars.b = tk.StringVar(self.controls_frame)
        r_spinbox = tk.Spinbox(self.controls_frame, width=4, from_=0, to=255, textvariable=tk_vars.r, wrap=True,
                               command=rgb_command)
        g_spinbox = tk.Spinbox(self.controls_frame, width=4, from_=0, to=255, textvariable=tk_vars.g, wrap=True,
                               command=rgb_command)
        b_spinbox = tk.Spinbox(self.controls_frame, width=4, from_=0, to=255, textvariable=tk_vars.b, wrap=True,
                               command=rgb_command)
        r_spinbox.bind('<' + EVENT_FLAG_ENTERKEY + '>', rgb_event_command)
        g_spinbox.bind('<' + EVENT_FLAG_ENTERKEY + '>', rgb_event_command)
        b_spinbox.bind('<' + EVENT_FLAG_ENTERKEY + '>', rgb_event_command)

        tk_vars.common_colors = tk.StringVar(self.controls_frame)
        common_colors_label = tk.Label(self.controls_frame, text='Common Colors', wraplength=100, justify=tk.LEFT)
        common_colors_combobox = ttk.Combobox(self.controls_frame, width=10, textvariable=tk_vars.common_colors,
                                              values=COMMON_COLORS)
        common_colors_combobox.current(0)
        common_colors_combobox.bind('<<ComboboxSelected>>', common_colors_event_command)

        tk_vars.brush_size = tk.IntVar(self.controls_frame, value=config.BRUSH_SIZE)
        brush_size_label = tk.Label(self.controls_frame, text='Brush Size', wraplength=100, justify=tk.LEFT)
        brush_size_spinbox = tk.Spinbox(self.controls_frame, width=3, from_=1, to=15, textvariable=tk_vars.brush_size,
                                        wrap=True, command=brush_size_command)
        brush_size_spinbox.bind('<' + EVENT_FLAG_ENTERKEY + '>', brush_size_event_command)

        self.color_label.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky=tk.N + tk.S + tk.E + tk.W)
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
        file.add_command(label="New Image       Ctrl+N", command=file_new_image_command)
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
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-n>', file_new_image_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-s>', file_save_image_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-w>', file_close_window_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-z>', edit_undo_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-x>', edit_clear_all_key_command)

    def _add_widgets(self):
        self._add_menubar()
        self._add_image()
        self._add_controls()

    def close_window(self):
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
            self.close_window()
            self._new_window()


if __name__ == '__main__':
    root = tk.Tk()
    globals.input_image_window = InputImageWindow(root)
    btn = tk.Button(root, text="open", command=lambda: globals.input_image_window.
                    open_window('/home/bhavye/Desktop/DIP/Project/media/raw/tree.jpg'))
    btn.pack()
    root.mainloop()
