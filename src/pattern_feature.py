import numpy as np
from scipy import ndimage as ndi, signal
from skimage.filters import gabor


def pattern_features_of_image_from_filter_bank(img, filter_bank, mode='reflect'):
    pattern_features = []
    for filter in filter_bank:
        # pattern_feature = np.abs(signal.convolve(img, np.conjugate(filter), mode='same'))
        pattern_feature = np.abs(ndi.convolve(img, np.conjugate(filter), mode=mode))
        pattern_features.append(pattern_feature)
    return pattern_features


def pattern_features_of_image_using_skimage(img, N=6, sigmas=(1, 3), freqs=(0.5, 0.25), mode='reflect', cval=0):
    pattern_features = []
    for n in range(N):
        theta = (n * np.pi) / N
        for sigma in sigmas:
            for freq in freqs:
                filtered_real, _ = gabor(img, freq, theta=theta, sigma_x=sigma, sigma_y=sigma, mode=mode, cval=cval)
                pattern_features.append(filtered_real)
    return pattern_features
