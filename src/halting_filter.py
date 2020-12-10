from src.utils import *


def halting_filter(img, lsm_type):
    if lsm_type == 'intensity':
        return halting_filter_intensity(img)
    elif lsm_type == 'pattern':
        return halting_filter_pattern(img)
    else:
        print(f'Invalid lsm_type {lsm_type}! Valid lsm_type are [\'intensity\', \'pattern\']')


def halting_filter_intensity(img, sigma=1):
    gaussian_smoothed_img = ndi.gaussian_filter(img, sigma)
    mag_grad_img = mag_grad2d(*np.gradient(gaussian_smoothed_img))
    hI = 1 / (1 + mag_grad_img)
    return hI


def halting_filter_pattern(img):
    pass
