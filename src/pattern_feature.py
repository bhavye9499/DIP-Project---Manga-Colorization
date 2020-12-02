import numpy as np
from scipy import signal


def pattern_features_of_image(img, filter_bank):
    pattern_features = []
    for filter in filter_bank:
        pattern_feature = np.abs(signal.convolve(img, np.conjugate(filter), mode='same'))
        pattern_features.append(pattern_feature)
    return pattern_features
