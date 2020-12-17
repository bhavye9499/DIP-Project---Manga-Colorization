import numpy as np
from scipy import ndimage as ndi
from skimage.filters import gabor
from tqdm import tqdm

from src.globals import config, globals
from src.globals.constants import Region
from src.utils import utils


def halting_filter(raw_img):
    if config.REGION == Region.intensity:
        return halting_filter_intensity(raw_img)
    elif config.REGION == Region.pattern:
        return halting_filter_pattern(raw_img)
    else:
        raise ValueError(f'Invalid region {config.REGION}! Valid lsm_type are {[e for e in Region]}')


def halting_filter_intensity(img):
    gaussian_smoothed_img = ndi.gaussian_filter(img, config.GAUSSIAN_SIGMA)
    mag_grad_img = utils.mag_grad2d(*np.gradient(gaussian_smoothed_img))
    hI = 1 / (1 + mag_grad_img ** 2)
    return hI


def halting_filter_pattern(img):
    check_distance_map()

    # hP = 1 / (1 + np.abs(globals.distance_map))

    clustered_img_fvs = utils.perform_clustering(globals.img_fvs, config.CLUSTERS)
    hP = clustered_img_fvs[:, :, 0] == clustered_img_fvs[config.START_PIXEL[::-1]][0]
    hP = hP & (clustered_img_fvs[:, :, 1] == clustered_img_fvs[config.START_PIXEL[::-1]][1])
    hP = hP & (clustered_img_fvs[:, :, 2] == clustered_img_fvs[config.START_PIXEL[::-1]][2])
    hP = np.asarray(hP, dtype=np.int)

    return hP


# Helper functions for halting_filter_patter()
# --------------------------------------------------
def check_distance_map():
    check_image_feature_vectors()
    if globals.distance_map is None:
        raw_img_arr = np.asarray(globals.raw_img)
        user_fv = user_feature_vector(globals.img_fvs)
        globals.distance_map = distance_map(raw_img_arr.shape, globals.img_fvs, user_fv)


def check_image_feature_vectors():
    if globals.img_fvs is None or globals.orientations_changed or globals.gabor_sigmas_changed:
        raw_img_arr = np.asarray(globals.raw_img)
        freqs = utils.get_frequencies(raw_img_arr.shape)
        pattern_features = image_pattern_features(raw_img_arr, config.ORIENTATIONS, config.GABOR_SIGMAS, freqs)
        filter_bank_size = config.ORIENTATIONS * len(config.GABOR_SIGMAS) * len(freqs)
        globals.img_fvs = image_feature_vectors(raw_img_arr.shape, pattern_features, filter_bank_size)
        globals.orientations_changed = False
        globals.gabor_sigmas_changed = False


def distance_map(shape, img_feature_vector_set, feature_vector_user):
    output = np.zeros(shape, dtype=np.float_)
    P, Q = shape
    for i in range(P):
        for j in range(Q):
            feature_vector_front = img_feature_vector_set[i, j]
            output[i, j] = feature_dist(feature_vector_user, feature_vector_front)
    return output


def feature_dist(fv1, fv2):
    """
    Return the feature distance between feature vectors fv1 and fv2.
    The sum of square difference is the distance measure.
    """
    diff = fv1 - fv2
    return np.dot(diff, diff)


def image_feature_vectors(shape, pattern_features, filter_bank_length):
    """
    Returns pattern feature vector set of the image.
    The feature vector contains 2 * len(filter_bank) values.
    Mean and Standard deviation for each filter in filter bank.
    """
    P, Q = shape
    img_feature_vector_set = np.zeros((P, Q, 2 * filter_bank_length), dtype=np.float_)
    for i in tqdm(range(len(pattern_features))):
        pattern_feature_mean = ndi.generic_filter(np.real(pattern_features[i]), np.mean, size=config.WINDOW_SIZE)
        pattern_feature_std = ndi.generic_filter(np.real(pattern_features[i]), np.std, size=config.WINDOW_SIZE)
        img_feature_vector_set[:, :, 2 * i] = pattern_feature_mean
        img_feature_vector_set[:, :, 2 * i + 1] = pattern_feature_std
    return img_feature_vector_set


def image_pattern_features(img, N, sigmas, freqs):
    pattern_features = []
    for n in range(N):
        theta = (n * np.pi) / N
        for sigma in sigmas:
            for freq in freqs:
                filtered_real, filtered_img = gabor(img, freq, theta=theta, sigma_x=sigma, sigma_y=sigma)
                pattern_features.append(filtered_real + np.complex(0, 1) * filtered_img)
    return pattern_features


def user_feature_vector(img_fvs):
    feature_vectors = []
    for (x, y) in globals.scribbled_pixels:
        feature_vectors.append(img_fvs[y, x])
    user_fv = np.average(feature_vectors, axis=0)
    return user_fv
