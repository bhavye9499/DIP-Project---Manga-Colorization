import numpy as np

from src.utils import *
from src.visualizer import visualize_feature_vectors


def feature_vector_at_pixel(location, img_pattern_features, filter_bank):
    """
    Return the local pattern feature vector at coordinates (x, y).
    The feature vector contains 2 * len(filter_bank) values.
    Mean and Standard deviation for each filter in filter bank.
    """
    feature_vector = []
    for pattern_feature, filter in zip(img_pattern_features, filter_bank):
        mat = get_pixel_neighbourhood(pattern_feature, location, filter.shape)
        feature_vector.append(np.mean(mat))
        feature_vector.append(np.std(mat))
    return feature_vector


def feature_vector_user(raw_img, scribbled_img, img_pattern_features, filter_bank, delta=5):
    """
    Return a pattern feature vector for a scribble.
    The feature vector contains 2 * len(filter_bank) values.
    Mean and Standard deviation for each filter in filter bank.
    """
    P, Q = raw_img.shape
    feature_vectors = []
    for x in range(P):
        for y in range(Q):
            pixel = scribbled_img[x, y]
            if max(pixel) - min(pixel) > delta:
                feature_vector = feature_vector_at_pixel((x, y), img_pattern_features, filter_bank)
                feature_vectors.append(feature_vector)
    # visualize_feature_vectors(feature_vectors)
    feature_vector_user = np.mean(feature_vectors, axis=0)  # TODO find feature_vector_user using clustering methods
    return feature_vector_user
