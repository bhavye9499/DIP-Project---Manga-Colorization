from os import path, pardir
from tkinter import messagebox

# for GUI windows
home_window = None
input_image_window = None
output_image_window = None

# for opening/saving images
filename = None
save_dir = path.join(path.dirname(path.abspath(__file__)), pardir, pardir, 'media', 'output')  # TODO change to '/'
search_dir = path.join(path.dirname(path.abspath(__file__)), pardir, pardir, 'media', 'input')  # TODO change to '/'

# for brush-stroking
drawing = False

# for input, scribbled, output images
raw_img = None
prev_scribbled_img = None
curr_scribbled_img = None
prev_output_img = None
curr_output_img = None

# for halting filter for pattern
distance_map = None
img_fvs = None
orientations_changed = False
gabor_sigmas_changed = False

# for level set method
scribbled_pixels = None
phi = None


def info_message(message):
    messagebox.showinfo('Info', message)


def reset_globals():
    global distance_map, img_fvs, orientations_changed, gabor_sigmas_changed

    distance_map = None
    img_fvs = None
    orientations_changed = False
    gabor_sigmas_changed = False
