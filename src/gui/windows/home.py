import tkinter as tk

from src.gui.commands.home_commands import *


class HomeWindow:
    def __init__(self, master):
        self.master = master

    def _add_heading(self):
        self.heading = tk.Label(self.master, text='Manga Colorization', font=("Courier", 24, 'bold'), padx=5, pady=5)
        self.heading.pack()

    def _add_menubar(self):
        self.menubar = tk.Menu(self.master)

        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label="Open Image", command=file_open_image_command)
        file.add_separator()
        file.add_command(label="Exit", command=self._close_window)

        edit = tk.Menu(self.menubar, tearoff=0)

        region = tk.Menu(edit, tearoff=0)
        self.region_variable = tk.IntVar()
        region.add_radiobutton(label='Intensity-continuous', variable=self.region_variable, value=1,
                               command=edit_region_command)
        region.add_radiobutton(label='Pattern-continuous', variable=self.region_variable, value=2,
                               command=edit_region_command)
        self.region_variable.set(1)

        intensity_params = tk.Menu(edit, tearoff=0)
        intensity_params.add_command(label='Gaussian sigma', command=edit_gaussian_sigma_command)

        pattern_params = tk.Menu(edit, tearoff=0)
        pattern_params.add_command(label='Gabor Sigmas', command=edit_gabor_sigmas_command)
        pattern_params.add_command(label='Orientations', command=edit_orientations_command)
        pattern_params.add_command(label='Window Size', command=edit_window_size_command)

        lsm_params = tk.Menu(edit, tearoff=0)
        lsm_params.add_command(label='Break-off threshold', command=edit_break_off_threshold_command)
        lsm_params.add_command(label='Display Step', command=edit_display_step_command)
        lsm_params.add_command(label='Epsilon', command=edit_epsilon_command)
        lsm_params.add_command(label='FA', command=edit_fa_command)
        lsm_params.add_command(label='Relaxation Factor', command=edit_relaxation_factor_command)
        lsm_params.add_command(label='Re-initializations', command=edit_re_initializations_command)
        lsm_params.add_command(label='Time Step (dt)', command=edit_time_step_command)

        edit.add_cascade(label='Region', menu=region)
        edit.add_cascade(label='Intensity Params', menu=intensity_params)
        edit.add_cascade(label='Pattern Params', menu=pattern_params)
        edit.add_cascade(label='LSM Params', menu=lsm_params)

        view = tk.Menu(self.menubar, tearoff=0)
        view.add_command(label="Intensity Params")
        view.add_command(label="Pattern Params")
        view.add_command(label="LSM Params")
        view.add_separator()
        view.add_command(label="Clear Screen")

        option = tk.Menu(self.menubar, tearoff=0)
        option.add_command(label="Start Segmentation")
        option.add_command(label="Stop Segmentation")

        help = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="File", menu=file)
        self.menubar.add_cascade(label="Edit", menu=edit)
        self.menubar.add_cascade(label="View", menu=view)
        self.menubar.add_cascade(label="Option", menu=option)
        self.menubar.add_cascade(label="Help", menu=help)

        self.master.config(menu=self.menubar)

    def _add_widgets(self):
        self._add_menubar()
        self._add_heading()

    def _close_window(self):
        self.master.quit()

    def _new_window(self):
        self.master.title('Manga Colorization')
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.columnconfigure(self.master, 0, weight=1)
        self._add_widgets()
        self.master.mainloop()

    def open_window(self):
        if self.master is None:
            self._new_window()
        else:
            self._close_window()
            self._new_window()


if __name__ == '__main__':
    root = tk.Tk()
    home_screen = HomeWindow(root)
    home_screen.open_window()
