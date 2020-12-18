from copy import deepcopy
from os import path
from PIL import ImageTk
from tkinter import filedialog

from src.globals import globals
from src.globals.constants import *


# Menubar commands
# ----------------------------------------
def file_close_window_key_command(event):
    globals.output_image_window.close_window()


def file_save_image_command():
    save_as_filename = filedialog.asksaveasfilename(initialdir=globals.save_dir, title='Save Image As',
                                                    filetypes=FILE_TYPES)
    if save_as_filename:
        globals.save_dir = path.dirname(save_as_filename)
        filename, file_extension = path.splitext(save_as_filename)

        if file_extension == '':
            file_extension = FORMAT_PNG
        else:
            file_extension = file_extension[1:]

        filename = filename + '.' + file_extension

        if file_extension == FORMAT_JPG or file_extension == FORMAT_JPEG:
            globals.curr_output_img.convert('RGB').save(filename, format=file_extension)
        else:
            globals.curr_output_img.save(filename, format=file_extension)


def file_save_image_key_command(event):
    file_save_image_command()


def edit_clear_all_command():
    globals.prev_output_img = deepcopy(globals.curr_output_img)
    globals.curr_output_img = deepcopy(globals.raw_img).convert('RGB')
    update_output_image()


def edit_clear_all_key_command(event):
    edit_clear_all_command()


def edit_undo_command():
    if globals.prev_output_img is not None:
        globals.curr_output_img = globals.prev_output_img
        globals.prev_output_img = None
        update_output_image()


def edit_undo_key_command(event):
    edit_undo_command()


def update_output_image():
    global img
    img = ImageTk.PhotoImage(globals.curr_output_img)
    globals.output_image_window.img_label.config(image=img)
