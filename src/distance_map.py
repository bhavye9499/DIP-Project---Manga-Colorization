from tqdm import tqdm

from src.feature_vector import *


def feature_dist(fv1, fv2):
    """
    Return the feature distance between feature vectors fv1 and fv2.
    The sum of square difference is the distance measure.
    """
    diff = fv1 - fv2
    return np.dot(diff, diff)


def distance_map(shape, img_pattern_features, filter_bank, feature_vector_user):
    output = np.zeros(shape, dtype=np.float_)
    P, Q = shape
    for i in tqdm(range(P)):
        for j in range(Q):
            feature_vector_front = feature_vector_at_pixel((i, j), img_pattern_features, filter_bank)
            output[i, j] = feature_dist(feature_vector_user, feature_vector_front)
    return output
