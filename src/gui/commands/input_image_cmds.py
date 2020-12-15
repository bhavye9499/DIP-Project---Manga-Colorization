import numpy as np
from PIL import ImageDraw, ImageTk

from src.globals import globals, config, tkinter_variables as tk_vars
from src.globals.constants import *
from src.utils import utils


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


def draw_circle(event):
    draw = ImageDraw.Draw(globals.curr_scribbled_img)
    leftUpPoint = (event.x - config.BRUSH_SIZE, event.y - config.BRUSH_SIZE)
    rightDownPoint = (event.x + config.BRUSH_SIZE, event.y + config.BRUSH_SIZE)
    twoPointList = [leftUpPoint, rightDownPoint]
    r_val = int(tk_vars.r.get())
    g_val = int(tk_vars.g.get())
    b_val = int(tk_vars.b.get())
    draw.ellipse(twoPointList, fill=(r_val, g_val, b_val))
    global img
    img = ImageTk.PhotoImage(globals.curr_scribbled_img)
    globals.input_image_window.img_label.config(image=img)


def brush_stroke_command(event):
    if str(event.type) == EVENT_LBUTTONDOWN:
        globals.drawing = True

    elif str(event.type) == EVENT_MOUSEMOVE:
        if globals.drawing:
            draw_circle(event)

    elif str(event.type) == EVENT_LBUTTONUP:
        globals.drawing = False
        draw_circle(event)
        globals.prev_scribbled_img = globals.curr_scribbled_img


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
