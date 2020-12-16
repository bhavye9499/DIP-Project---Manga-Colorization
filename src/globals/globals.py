from os import path, pardir
from tkinter import messagebox

home_window = None
input_image_window = None
output_image_window = None

filename = None
save_dir = path.join(path.dirname(path.abspath(__file__)), pardir, pardir, 'media', 'output')  # TODO change to '/'
search_dir = path.join(path.dirname(path.abspath(__file__)), pardir, pardir, 'media', 'input')  # TODO change to '/'

drawing = False

raw_img = None
prev_scribbled_img = None
curr_scribbled_img = None
prev_output_img = None
curr_output_img = None

phi = None


def info_message(message):
    messagebox.showinfo('Info', message)
