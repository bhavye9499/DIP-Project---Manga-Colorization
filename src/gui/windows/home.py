import tkinter as tk

from src.globals.constants import *
from src.gui.commands.home_cmds import *


class HomeWindow:
    def __init__(self, master):
        self.master = master

    def _add_heading(self):
        self.heading = tk.Label(self.master, text='Manga Colorization', font=('Ubuntu', 24, 'bold'), padx=5, pady=5)
        self.heading.pack()

    def _add_menubar(self):
        self.menubar = tk.Menu(self.master)

        file = tk.Menu(self.menubar, tearoff=0)
        file.add_command(label='Open Image    Ctrl+O', command=file_open_image_command)
        file.add_separator()
        file.add_command(label='Exit Program   Ctrl+Q', command=self.close_window)

        edit = tk.Menu(self.menubar, tearoff=0)

        region = tk.Menu(edit, tearoff=0)
        tk_vars.region = tk.IntVar(self.master)
        region.add_radiobutton(label='Intensity-continuous', variable=tk_vars.region, value=Region.intensity.value,
                               command=edit_region_command)
        region.add_radiobutton(label='Pattern-continuous', variable=tk_vars.region, value=Region.pattern.value,
                               command=edit_region_command)
        tk_vars.region.set(config.REGION.value)

        colorization_method = tk.Menu(edit, tearoff=0)
        tk_vars.colorization_method = tk.IntVar(self.master)
        colorization_method.add_radiobutton(label='Color Replacement', variable=tk_vars.colorization_method,
                                            value=Colorization.color_replacement.value,
                                            command=edit_colorization_method_command)
        colorization_method.add_radiobutton(label='Pattern to Shading', variable=tk_vars.colorization_method,
                                            value=Colorization.pattern_to_shading.value,
                                            command=edit_colorization_method_command)
        colorization_method.add_radiobutton(label='Stroke-Preserving', variable=tk_vars.colorization_method,
                                            value=Colorization.stroke_preserving.value,
                                            command=edit_colorization_method_command)
        tk_vars.colorization_method.set(config.COLORIZATION_METHOD.value)

        intensity_params = tk.Menu(edit, tearoff=0)
        intensity_params.add_command(label='Gaussian sigma', command=edit_gaussian_sigma_command)
        leak_proofing = tk.Menu(intensity_params, tearoff=0)
        tk_vars.leak_proofing = tk.BooleanVar(self.master)
        leak_proofing.add_radiobutton(label='Enable', variable=tk_vars.leak_proofing,
                                      value=True, command=edit_leak_proofing_command)
        leak_proofing.add_radiobutton(label='Disable', variable=tk_vars.leak_proofing,
                                      value=False, command=edit_leak_proofing_command)
        tk_vars.leak_proofing.set(config.LEAK_PROOFING)
        intensity_params.add_cascade(label='Leak Proofing', menu=leak_proofing)

        pattern_params = tk.Menu(edit, tearoff=0)
        pattern_params.add_command(label='Clusters', command=edit_clusters_command)
        pattern_params.add_command(label='Gabor Sigmas', command=edit_gabor_sigmas_command)
        pattern_params.add_command(label='Orientations', command=edit_orientations_command)
        pattern_params.add_command(label='Window Size', command=edit_window_size_command)

        lsm_params = tk.Menu(edit, tearoff=0)
        lsm_params.add_command(label='Break-off threshold', command=edit_break_off_threshold_command)
        lsm_params.add_command(label='Display Step', command=edit_display_step_command)
        lsm_params.add_command(label='Curvature Coefficient', command=edit_curvature_coefficient_command)
        lsm_params.add_command(label='Ballooning Force', command=edit_ballooning_force_command)
        lsm_params.add_command(label='Maximum Iterations', command=edit_max_iterations_command)
        lsm_params.add_command(label='Relaxation Factor', command=edit_relaxation_factor_command)
        lsm_params.add_command(label='Re-initializations', command=edit_re_initializations_command)
        lsm_params.add_command(label='Time Step (dt)', command=edit_time_step_command)

        edit.add_cascade(label='Region', menu=region)
        edit.add_cascade(label='Colorization Method', menu=colorization_method)
        edit.add_cascade(label='Intensity Params', menu=intensity_params)
        edit.add_cascade(label='Pattern Params', menu=pattern_params)
        edit.add_cascade(label='LSM Params', menu=lsm_params)

        view = tk.Menu(self.menubar, tearoff=0)
        view.add_command(label='Clustered Image Feature Vectors')
        view.add_command(label='Distance Map')
        view.add_command(label='Halting Filter Intensity')
        view.add_command(label='Halting Filter Pattern')
        view.add_command(label='Intensity Params')
        view.add_command(label='Pattern Params')
        view.add_command(label='LSM Params')
        view.add_separator()
        view.add_command(label='Clear Screen')

        option = tk.Menu(self.menubar, tearoff=0)
        option.add_command(label='Start Segmentation', command=option_start_segmentation_command)
        option.add_command(label='Stop Segmentation', command=option_stop_segmentation_command)
        option.add_separator()
        option.add_command(label='Perform Colorization', command=option_perform_colorization_command)
        # option.add_command(label='Redo Colorization', command=option_redo_colorization_command)

        help = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label='File', menu=file)
        self.menubar.add_cascade(label='Edit', menu=edit)
        self.menubar.add_cascade(label='View', menu=view)
        self.menubar.add_cascade(label='Option', menu=option)
        self.menubar.add_cascade(label='Help', menu=help)

        self.master.config(menu=self.menubar)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-o>', file_open_image_key_command)
        self.master.bind('<' + EVENT_FLAG_CTRLKEY + '-' + EVENT_FLAG_KEYPRESS + '-q>', file_close_window_key_command)

    def _add_widgets(self):
        self._add_menubar()
        self._add_heading()

    def close_window(self):
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
            self.close_window()
            self._new_window()


if __name__ == '__main__':
    root = tk.Tk()
    home_screen = HomeWindow(root)
    home_screen.open_window()
