import numpy as np
from copy import deepcopy
from os import path
from tkinter import simpledialog, filedialog

from src.colorizer import pattern_to_shading, strokePreservingColorization
from src.level_set_method import perform_LSM
from src.globals import config, globals, tkinter_variables as tk_vars
from src.globals.constants import Colorization, FILE_TYPES, Region
from src.gui.commands.output_image_cmds import update_output_image


def edit_ballooning_force_command():
    response = simpledialog.askfloat(title='Ballooning Force', prompt='Ballooning Force:', initialvalue=config.FA)
    if isinstance(response, float):
        config.FA = response


def edit_break_off_threshold_command():
    response = simpledialog.askinteger(title='Break-off Threshold', prompt='Break-off Threshold:',
                                       initialvalue=config.LSM_THRESHOLD, minvalue=1)
    if isinstance(response, int):
        config.LSM_THRESHOLD = response


def edit_clusters_command():
    response = simpledialog.askinteger(title='Clusters', prompt='Clusters:', initialvalue=config.CLUSTERS,
                                       minvalue=1)
    if isinstance(response, int):
        config.CLUSTERS = response


def edit_curvature_coefficient_command():
    response = simpledialog.askfloat(title='Curvature Coefficient', prompt='Curvature Coefficient:',
                                     initialvalue=config.EPSILON)
    if isinstance(response, float):
        config.EPSILON = response


def edit_display_step_command():
    response = simpledialog.askinteger(title='Display Step', prompt='Display Step:', initialvalue=config.DISPLAY_STEP,
                                       minvalue=1)
    if isinstance(response, int):
        config.DISPLAY_STEP = response


def edit_colorization_method_command():
    config.COLORIZATION_METHOD = Colorization(tk_vars.colorization_method.get())


def edit_gabor_sigmas_command():
    response = simpledialog.askstring(title='Gabor Sigmas', prompt='Gabor Sigmas:',
                                      initialvalue=config.SIGMAS)
    if isinstance(response, str):
        config.SIGMAS = response.split(' ')
        print(config.SIGMAS)


def edit_gaussian_sigma_command():
    response = simpledialog.askfloat(title='Gaussian Sigma', prompt='Gaussian Sigma:', initialvalue=config.SIGMA)
    if isinstance(response, float):
        config.SIGMA = response


def edit_orientations_command():
    response = simpledialog.askinteger(title='Orientations', prompt='Orientations:', initialvalue=config.ORIENTATIONS,
                                       minvalue=1)
    if isinstance(response, int):
        config.ORIENTATIONS = response


def edit_max_iterations_command():
    response = simpledialog.askinteger(title='Maximum Iterations', prompt='Maximum Iterations:',
                                       initialvalue=config.MAX_ITERATIONS, minvalue=1)
    if isinstance(response, int):
        config.MAX_ITERATIONS = response


def edit_relaxation_factor_command():
    response = simpledialog.askfloat(title='Relaxation Factor', prompt='Relaxation Factor:',
                                     initialvalue=config.RELAX_FACTOR)
    if isinstance(response, float):
        config.RELAX_FACTOR = response


def edit_re_initializations_command():
    response = simpledialog.askinteger(title='Re-initializations', prompt='Re-initializations:', initialvalue=config.NR,
                                       minvalue=1)
    if isinstance(response, int):
        config.NR = response


def edit_region_command():
    config.REGION = Region(tk_vars.region.get())


def edit_leak_proofing_command():
    config.LEAK_PROOFING = tk_vars.leak_proofing.get()


def edit_time_step_command():
    response = simpledialog.askfloat(title='Time Step (dt)', prompt='Time Step (dt):', initialvalue=config.DT)
    if isinstance(response, float):
        config.DT = response


def edit_window_size_command():
    response = simpledialog.askinteger(title='Window Size', prompt='Window Size:', initialvalue=config.WINDOW_SIZE,
                                       minvalue=1)
    if isinstance(response, int):
        config.WINDOW_SIZE = response


def file_close_window_key_command(event):
    globals.home_window.close_window()


def file_open_image_command():
    globals.filename = filedialog.askopenfilename(initialdir=globals.search_dir, title='Open Image',
                                                  filetypes=FILE_TYPES)
    if globals.filename:
        globals.search_dir = path.dirname(globals.filename)
        globals.input_image_window.open_window(globals.filename)
        globals.output_image_window.open_window(globals.filename)


def file_open_image_key_command(event):
    file_open_image_command()


def option_perform_colorization_command():
    globals.prev_output_img = deepcopy(globals.curr_output_img)

    r_val = int(tk_vars.r.get())
    g_val = int(tk_vars.g.get())
    b_val = int(tk_vars.b.get())
    color = np.array([r_val, g_val, b_val])

    colorization_method = Colorization(tk_vars.colorization_method.get())

    if colorization_method == Colorization.pattern_to_shading:
        pattern_to_shading(color)

    elif colorization_method == Colorization.stroke_preserving:
        strokePreservingColorization(color)

    print('hi')

    update_output_image()


def option_start_segmentation_command():
    perform_LSM()


def option_stop_segmentation_command():
    config.CONTINUE_LSM = False
