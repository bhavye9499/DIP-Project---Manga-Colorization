from src.generic_imports import *
from src.utils import *


def get_halting_filter_intensity(img, sigma=1):
    gaussian_smoothed_img = ndi.gaussian_filter(img, sigma)
    mag_grad_img = mag_grad2d(*np.gradient(gaussian_smoothed_img))
    hI = 1 / (1 + mag_grad_img)
    # gaussian = cv2.GaussianBlur(img, (3, 3), 0)
    # h1 = 1 / (1 + np.abs(cv2.Laplacian(gaussian, -1)))
    # hI = np.power(np.abs(1 - h1), 2)
    # Image.fromarray(log_transform(hI)).show()
    return hI


def get_halting_filter_pattern(img):
    pass
