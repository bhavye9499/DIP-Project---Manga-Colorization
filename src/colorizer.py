import cv2
import numpy as np

from src.utils.utils import map_mat


def rgb2yuv(color):
    """
    Converts the rgb color to yuv color
    :param color: (r, g, b) color
    :return: (y, u, v) color
    """
    yuv_img = cv2.cvtColor(np.array([[color]]), cv2.COLOR_BGR2YUV)
    return yuv_img[0][0]


def patternToShading(image, mask, color):
    """
    Perform shading of the masked region with the given RGB color
    and return the image in RGB format.
    image: Image array in grayscale format
    mask: array of 0s and 1s with same shape of image array
    color: (r, g, b) color to shade the masked region
    """
    yuv_image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2YUV)
    y_user, u_user, v_user = rgb2yuv(color)

    # Extract YUV channels
    y, u, v = cv2.split(yuv_image)
    y_new, u_new, v_new = y.copy(), u.copy(), v.copy()

    # Filter y channel with box filter
    s = cv2.boxFilter(y, -1, (3, 3), (-1, -1))
    s = (s - s.min()) / (s.max() - s.min())  # Normalize to range [0, 1]

    # Calculate new YUV channels
    y_new[mask == 1] = (y_user * s)[mask == 1]
    u_new[mask == 1] = u_user
    v_new[mask == 1] = v_user

    new_image = cv2.merge((y_new, u_new, v_new))

    return cv2.cvtColor(new_image, cv2.COLOR_YUV2RGB)


def strokePreservingColorization(image, mask, color, gauss_size=(7, 7), alpha=0.8):
    """
    Perform stroke preserving colorization of the masked region
    with the given YUV color and return the image in RGB format.
    image: Image array in grayscale format
    mask: array of 0s and 1s with same shape of image array
    color: (y, u, v) color to colorize the masked region
    """
    yuv_image = cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2YUV)
    y_user, u_user, v_user = rgb2yuv(color)

    # Extract YUV channels
    y, u, v = cv2.split(yuv_image)
    y_new, u_new, v_new = y.copy(), u.copy(), v.copy()

    gaussian = cv2.GaussianBlur(image, gauss_size, 0)
    h1 = 1 / (1 + np.abs(cv2.Laplacian(gaussian, -1)))
    kernel = map_mat(np.square(np.abs(1 - h1)))

    # Calculate new YUV channels
    y_new[(mask == 1) & (kernel > alpha)] = (y_user * kernel)[(mask == 1) & (kernel > alpha)]
    u_new[(mask == 1) & (kernel > alpha)] = u_user
    v_new[(mask == 1) & (kernel > alpha)] = v_user

    new_image = cv2.merge((y_new, u_new, v_new))

    return cv2.cvtColor(new_image, cv2.COLOR_YUV2RGB)
