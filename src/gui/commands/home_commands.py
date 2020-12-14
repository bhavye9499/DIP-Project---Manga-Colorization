from os import path
from tkinter import simpledialog, filedialog

from src import config
from src.gui import globals
from src.gui.constants import FILE_TYPES


def edit_break_off_threshold_command():
    response = simpledialog.askinteger(title='Break-off Threshold', prompt='Break-off Threshold:',
                                       initialvalue=config.LSM_THRESHOLD)
    if isinstance(response, int):
        config.LSM_THRESHOLD = response


def edit_display_step_command():
    response = simpledialog.askinteger(title='Display Step', prompt='Display Step:', initialvalue=config.DISPLAY_STEP,
                                       minvalue=1)
    if isinstance(response, int):
        config.DISPLAY_STEP = response


def edit_epsilon_command():
    response = simpledialog.askfloat(title='Epsilon', prompt='Epsilon:', initialvalue=config.EPSILON)
    if isinstance(response, float):
        config.EPSILON = response


def edit_fa_command():
    response = simpledialog.askfloat(title='FA', prompt='FA:', initialvalue=config.FA)
    if isinstance(response, float):
        config.FA = response


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
    config.REGION = globals.home_window.region_variable


def edit_time_step_command():
    response = simpledialog.askfloat(title='Time Step (dt)', prompt='Time Step (dt):', initialvalue=config.DT)
    if isinstance(response, float):
        config.DT = response


def edit_window_size_command():
    response = simpledialog.askinteger(title='Window Size', prompt='Window Size:', initialvalue=config.WINDOW_SIZE,
                                       minvalue=1)
    if isinstance(response, int):
        config.WINDOW_SIZE = response


def file_open_image_command():
    config.FILENAME = filedialog.askopenfilename(initialdir=globals.search_dir, title='Select An Image',
                                                 filetypes=FILE_TYPES)
    if config.FILENAME:
        globals.search_dir = path.dirname(config.FILENAME)
        globals.input_image_window.open_window(config.FILENAME)
        globals.output_image_window.open_window(config.FILENAME)
