import numpy as np
from copy import deepcopy
from os import path
from tkinter import simpledialog, filedialog

from src.colorizer import color_replacement, pattern_to_shading, stroke_preserving
from src.halting_filter import (
    check_distance_map,
    check_image_feature_vectors,
    halting_filter_intensity,
    halting_filter_pattern,
)
from src.level_set_method import perform_LSM
from src.globals import config, globals, tkinter_variables as tk_vars
from src.globals.constants import Colorization, FILE_TYPES, Region
from src.gui.commands.output_image_cmds import update_output_image
from src.utils import utils, visualizer


def edit_alpha_command():
    response = simpledialog.askfloat(title='Stroke Preserving Alpha', prompt='Stroke Preserving Alpha:',
                                     initialvalue=config.ALPHA)
    if isinstance(response, float):
        config.ALPHA = response


def edit_ballooning_force_command():
    response = simpledialog.askfloat(title='Ballooning Force', prompt='Ballooning Force:', initialvalue=config.FA)
    if isinstance(response, float):
        config.FA = response


def edit_break_off_threshold_command():
    response = simpledialog.askinteger(title='Break-off Threshold', prompt='Break-off Threshold:',
                                       initialvalue=config.LSM_THRESHOLD, minvalue=0)
    if isinstance(response, int):
        config.LSM_THRESHOLD = response


def edit_clusters_command():
    response = simpledialog.askinteger(title='Clusters', prompt='Clusters:', initialvalue=config.CLUSTERS,
                                       minvalue=1)
    if isinstance(response, int):
        config.CLUSTERS = response


def edit_colorization_method_command():
    config.COLORIZATION_METHOD = Colorization(tk_vars.colorization_method.get())


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


def edit_gabor_sigmas_command():
    response = simpledialog.askstring(title='Gabor Sigmas', prompt='Gabor Sigmas:',
                                      initialvalue=config.GABOR_SIGMAS)
    if isinstance(response, str):
        response = list(map(int, response.split(' ')))
        if config.GABOR_SIGMAS != response:
            globals.gabor_sigmas_changed = True
        config.GABOR_SIGMAS = response


def edit_gaussian_sigma_command():
    response = simpledialog.askfloat(title='Gaussian Sigma', prompt='Gaussian Sigma:',
                                     initialvalue=config.GAUSSIAN_SIGMA)
    if isinstance(response, float):
        config.GAUSSIAN_SIGMA = response


def edit_inverse_filter_command():
    config.INVERSE_FILTER = tk_vars.inverse_filter.get()


def edit_leak_proofing_command():
    config.LEAK_PROOFING = tk_vars.leak_proofing.get()


def edit_orientations_command():
    response = simpledialog.askinteger(title='Orientations', prompt='Orientations:', initialvalue=config.ORIENTATIONS,
                                       minvalue=1)
    if isinstance(response, int):
        if config.ORIENTATIONS != response:
            globals.orientations_changed = True
        config.ORIENTATIONS = response


def edit_max_iterations_command():
    response = simpledialog.askinteger(title='Maximum Iterations', prompt='Maximum Iterations:',
                                       initialvalue=config.MAX_ITERATIONS, minvalue=1)
    if isinstance(response, int):
        config.MAX_ITERATIONS = response


def edit_phi_threshold_command():
    response = simpledialog.askfloat(title='Phi Threshold', prompt='Phi Threshold:',
                                     initialvalue=config.PHI_THRESHOLD)
    if isinstance(response, float):
        config.PHI_THRESHOLD = response


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
    globals.reset_globals()
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

    color = np.asarray(globals.curr_scribbled_img)[config.START_PIXEL[::-1]]

    colorization_method = Colorization(tk_vars.colorization_method.get())

    if colorization_method == Colorization.color_replacement:
        color_replacement(color)

    elif colorization_method == Colorization.pattern_to_shading:
        pattern_to_shading(color)

    elif colorization_method == Colorization.stroke_preserving:
        stroke_preserving(color)

    update_output_image()


def option_redo_colorization_command():
    globals.prev_output_img = deepcopy(globals.curr_output_img)

    r_val = int(tk_vars.r.get())
    g_val = int(tk_vars.g.get())
    b_val = int(tk_vars.b.get())
    color = np.array([r_val, g_val, b_val])

    colorization_method = Colorization(tk_vars.colorization_method.get())

    if colorization_method == Colorization.color_replacement:
        color_replacement(color)

    elif colorization_method == Colorization.pattern_to_shading:
        pattern_to_shading(color)

    elif colorization_method == Colorization.stroke_preserving:
        stroke_preserving(color)

    update_output_image()


def option_start_segmentation_command():
    perform_LSM()


def option_stop_segmentation_command():
    config.CONTINUE_LSM = False


def view_distance_map_command():
    check_distance_map()
    visualizer.visualize_distance_map(255 - utils.normalize_and_scale(globals.distance_map), cmap='gray')


def view_halting_filter_intensity_command():
    raw_img_arr = deepcopy(np.asarray(globals.raw_img))
    hI = halting_filter_intensity(raw_img_arr)
    visualizer.visualize_halting_filter_intensity(hI)


def view_halting_filter_pattern_command():
    raw_img_arr = deepcopy(np.asarray(globals.raw_img))
    hP = halting_filter_pattern(raw_img_arr)
    visualizer.visualize_halting_filter_pattern(hP)


def view_image_feature_vectors_command():
    check_image_feature_vectors()
    visualizer.visualize_image_feature_vectors(globals.img_fvs, config.CLUSTERS)
