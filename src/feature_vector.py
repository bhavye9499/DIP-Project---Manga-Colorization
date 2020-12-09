from scipy import ndimage as ndi
from tqdm import tqdm

from src.utils import *
from src.visualizer import *


def feature_vector_set_of_image(shape, pattern_features, filter_bank_length, window_size=15, mode='reflect', cval=0):
    P, Q = shape
    img_feature_vector_set = np.zeros((P, Q, 2 * filter_bank_length), dtype=np.float_)
    for i in tqdm(range(len(pattern_features))):
        pattern_feature_mean = ndi.generic_filter(pattern_features[i], np.mean, size=window_size, mode=mode, cval=cval)
        pattern_feature_std = ndi.generic_filter(pattern_features[i], np.std, size=window_size, mode=mode, cval=cval)
        img_feature_vector_set[:, :, 2 * i] = pattern_feature_mean
        img_feature_vector_set[:, :, 2 * i + 1] = pattern_feature_std
    return img_feature_vector_set


def feature_vector_user(scribbled_img, img_feature_vector_set, delta=5):
    """
    Return a pattern feature vector for a scribble.
    The feature vector contains 2 * len(filter_bank) values.
    Mean and Standard deviation for each filter in filter bank.
    """
    scribbled_pixels = get_scribbled_pixels(scribbled_img, delta)
    feature_vectors = []
    for (x, y) in scribbled_pixels:
        feature_vectors.append(img_feature_vector_set[x, y])
    visualize_feature_vectors(feature_vectors)
    feature_vector_user = np.average(get_major_cluster(feature_vectors, eps=15, min_samples=10), axis=0)
    return feature_vector_user
