import numpy as np
from copy import deepcopy
from matplotlib import pyplot as plt
from os import path
from tkinter import filedialog
from PIL import ImageDraw, ImageTk

from src.globals import globals, config, tkinter_variables as tk_vars
from src.globals.constants import *
from src.gui.commands import home_cmds
from src.utils import utils


# Menubar commands
# ----------------------------------------
def file_close_window_key_command(event):
    globals.input_image_window.close_window()


def file_new_image_command():
    home_cmds.file_open_image_command()


def file_new_image_key_command(event):
    file_new_image_command()


def file_save_image_command():
    save_as_filename = filedialog.asksaveasfilename(initialdir=globals.save_dir, title='Save Image As',
                                                    filetypes=FILE_TYPES)
    if save_as_filename:
        globals.save_dir = path.dirname(save_as_filename)
        filename, file_extension = path.splitext(save_as_filename)
        file_extension = file_extension.lower()

        if file_extension == '':
            file_extension = FORMAT_PNG
        else:
            file_extension = file_extension[1:]

        filename = filename + '.' + file_extension

        if file_extension == FORMAT_JPG or file_extension == FORMAT_JPEG:
            globals.curr_scribbled_img.convert('RGB').save(filename, format=file_extension)
        else:
            globals.curr_scribbled_img.save(filename, format=file_extension)


def file_save_image_key_command(event):
    file_save_image_command()


def edit_clear_all_command():
    globals.prev_scribbled_img = deepcopy(globals.curr_scribbled_img)
    globals.curr_scribbled_img = deepcopy(globals.raw_img).convert('RGB')
    update_input_image()


def edit_clear_all_key_command(event):
    edit_clear_all_command()


def edit_undo_command():
    if globals.prev_scribbled_img is not None:
        globals.curr_scribbled_img = globals.prev_scribbled_img
        globals.prev_scribbled_img = None
        update_input_image()


def edit_undo_key_command(event):
    edit_undo_command()


def view_using_matplotlib_command():
    image = np.asarray(globals.curr_scribbled_img)
    plt.imshow(image)
    plt.show()


# Image commands
# ----------------------------------------
def brush_stroke_command(event):
    if str(event.type) == EVENT_LBUTTONDOWN:
        if PixelType(tk_vars.pixel_type.get()) == PixelType.start_pixel:
            config.START_PIXEL = (event.x, event.y)
        elif PixelType(tk_vars.pixel_type.get()) == PixelType.region_pixel:
            config.REGION_PIXEL = (event.x, event.y)
        # globals.reset_globals()
        globals.drawing = True
        globals.prev_scribbled_img = deepcopy(globals.curr_scribbled_img)
        globals.scribbled_pixels = np.array([[event.x, event.y]])

    elif str(event.type) == EVENT_MOUSEMOVE:
        if globals.drawing:
            globals.scribbled_pixels = np.append(globals.scribbled_pixels, [[event.x, event.y]], axis=0)
            draw_circle(event)

    elif str(event.type) == EVENT_LBUTTONUP:
        globals.drawing = False
        np.append(globals.scribbled_pixels, [[event.x, event.y]], axis=0)
        draw_circle(event)


def draw_circle(event):
    draw = ImageDraw.Draw(globals.curr_scribbled_img)
    leftUpPoint = (event.x - config.BRUSH_SIZE, event.y - config.BRUSH_SIZE)
    rightDownPoint = (event.x + config.BRUSH_SIZE, event.y + config.BRUSH_SIZE)
    twoPointList = [leftUpPoint, rightDownPoint]
    r_val = int(tk_vars.r.get())
    g_val = int(tk_vars.g.get())
    b_val = int(tk_vars.b.get())
    hex_val = utils.get_hex_from_rgb(r_val, g_val, b_val)
    draw.ellipse(twoPointList, fill=hex_val)
    update_input_image()


def update_input_image():
    global img
    img = ImageTk.PhotoImage(globals.curr_scribbled_img)
    globals.input_image_window.img_label.config(image=img)


# Controls commands
# ----------------------------------------
def brush_size_command():
    config.BRUSH_SIZE = int(tk_vars.brush_size.get())
    tk_vars.brush_size.set(str(np.clip(config.BRUSH_SIZE, 1, 15)))


def brush_size_event_command(event):
    brush_size_command()


def common_colors_event_command(event):
    color_name = tk_vars.common_colors.get()
    if color_name != '--Select--':
        color_hex = COMMON_COLORS_HEX_CODES[color_name]
        r_val, g_val, b_val = utils.get_rgb_from_hex(color_hex)
        tk_vars.r.set(r_val)
        tk_vars.g.set(g_val)
        tk_vars.b.set(b_val)
        globals.input_image_window.color_label.config(bg=color_hex)


def rgb_command():
    r_val = int(tk_vars.r.get())
    g_val = int(tk_vars.g.get())
    b_val = int(tk_vars.b.get())

    r_val = np.clip(r_val, 0, 255)
    g_val = np.clip(g_val, 0, 255)
    b_val = np.clip(b_val, 0, 255)

    tk_vars.r.set(r_val)
    tk_vars.g.set(g_val)
    tk_vars.b.set(b_val)
    tk_vars.common_colors.set(COMMON_COLORS[0])

    globals.input_image_window.color_label.config(bg=utils.get_hex_from_rgb(r_val, g_val, b_val))


def rgb_event_command(event):
    rgb_command()
