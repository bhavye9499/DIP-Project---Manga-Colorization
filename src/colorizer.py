import cv2
import numpy as np
from copy import deepcopy
from PIL import Image

from src.globals import config, globals
from src.utils.utils import map_mat, rgb2yuv


def color_replacement(color):
    output_image = deepcopy(np.asarray(globals.curr_output_img))
    color = color.astype(np.float)
    output_image[:, :, 0][globals.phi <= config.PHI_THRESHOLD] = color[0]
    output_image[:, :, 1][globals.phi <= config.PHI_THRESHOLD] = color[1]
    output_image[:, :, 2][globals.phi <= config.PHI_THRESHOLD] = color[2]
    globals.curr_output_img = Image.fromarray(output_image)


def pattern_to_shading(color):
    """
    Perform shading of the masked region with the given RGB color
    and return the image in RGB format.
    image: Image array in grayscale format
    mask: array of 0s and 1s with same shape of image array
    color: (r, g, b) color to shade the masked region
    """
    image = np.asarray(globals.curr_output_img)
    yuv_image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    y_user, u_user, v_user = rgb2yuv(color)

    # Extract YUV channels
    y, u, v = cv2.split(yuv_image)
    y_new, u_new, v_new = y.copy(), u.copy(), v.copy()

    # Filter y channel with box filter
    s = cv2.boxFilter(y, -1, (3, 3), (-1, -1))
    s = (s - s.min()) / (s.max() - s.min())  # Normalize to range [0, 1]

    # Creating mask for colorization
    mask = np.zeros_like(globals.phi)
    mask[globals.phi == 1] = 100
    mask[globals.phi <= 0] = 1

    # Calculate new YUV channels
    y_new[mask == 1] = (y_user * s)[mask == 1]
    u_new[mask == 1] = u_user
    v_new[mask == 1] = v_user

    new_image = cv2.merge((y_new, u_new, v_new))
    output_image = cv2.cvtColor(new_image, cv2.COLOR_YUV2RGB)
    globals.curr_output_img = Image.fromarray(output_image)


def stroke_preserving(color, gauss_size=(7, 7), alpha=0.8):
    """
    Perform stroke preserving colorization of the masked region
    with the given YUV color and return the image in RGB format.
    image: Image array in grayscale format
    mask: array of 0s and 1s with same shape of image array
    color: (y, u, v) color to colorize the masked region
    """
    image = np.asarray(globals.curr_output_img)
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    yuv_image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
    y_user, u_user, v_user = rgb2yuv(color)

    # Extract YUV channels
    y, u, v = cv2.split(yuv_image)
    y_new, u_new, v_new = y.copy(), u.copy(), v.copy()

    gaussian = cv2.GaussianBlur(gray_image, gauss_size, 0)
    h1 = 1 / (1 + np.abs(cv2.Laplacian(gaussian, -1)))
    kernel = map_mat(np.square(np.abs(1 - h1)))

    # Creating mask for colorization
    mask = np.zeros_like(globals.phi)
    mask[globals.phi == 1] = 100
    mask[globals.phi <= 0] = 1

    # Calculate new YUV channels
    y_new[(mask == 1) & (kernel > alpha)] = (y_user * kernel)[(mask == 1) & (kernel > alpha)]
    u_new[(mask == 1) & (kernel > alpha)] = u_user
    v_new[(mask == 1) & (kernel > alpha)] = v_user

    new_image = cv2.merge((y_new, u_new, v_new))
    output_img = cv2.cvtColor(new_image, cv2.COLOR_YUV2RGB)
    globals.curr_output_img = Image.fromarray(output_img)
