from scipy import ndimage as ndi
from skimage.filters import gabor
from tqdm import tqdm

from src.globals import config
from src.globals.constants import Region
from src.utils.utils import *


def halting_filter(raw_img, scribbled_img):
    if config.REGION == Region.intensity:
        return halting_filter_intensity(raw_img)
    elif config.REGION == Region.pattern:
        return halting_filter_pattern(raw_img, scribbled_img)
    else:
        raise ValueError(f'Invalid region {config.REGION}! Valid lsm_type are {[e for e in Region]}')


def halting_filter_intensity(img):
    gaussian_smoothed_img = ndi.gaussian_filter(img, config.SIGMA)
    mag_grad_img = mag_grad2d(*np.gradient(gaussian_smoothed_img))
    hI = 1 / (1 + mag_grad_img ** 2)
    return hI


# Helper functions for halting_filter_patter()
# --------------------------------------------------
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


def feature_vector_set_of_image(shape, pattern_features, filter_bank_length, window_size=15):
    """
    Returns pattern feature vector set of the image.
    The feature vector contains 2 * len(filter_bank) values.
    Mean and Standard deviation for each filter in filter bank.
    """
    P, Q = shape
    img_feature_vector_set = np.zeros((P, Q, 2 * filter_bank_length), dtype=np.float_)
    for i in tqdm(range(len(pattern_features))):
        pattern_feature_mean = ndi.generic_filter(np.real(pattern_features[i]), np.mean, size=window_size)
        pattern_feature_std = ndi.generic_filter(np.real(pattern_features[i]), np.std, size=window_size)
        img_feature_vector_set[:, :, 2 * i] = pattern_feature_mean
        img_feature_vector_set[:, :, 2 * i + 1] = pattern_feature_std
    return img_feature_vector_set


def feature_vector_user(scribbled_img, img_feature_vector_set, delta=5):
    scribbled_pixels = get_scribbled_pixels(scribbled_img, delta)
    feature_vectors = []
    for (x, y) in scribbled_pixels:
        feature_vectors.append(img_feature_vector_set[x, y])
    # major_cluster = get_major_cluster(feature_vectors, eps=15, min_samples=10)
    major_cluster = feature_vectors
    fv_user = np.average(major_cluster, axis=0)
    return fv_user


def pattern_features_of_image_using_skimage(img, N, sigmas, freqs, mode='reflect', cval=0):
    pattern_features = []
    for n in range(N):
        theta = (n * np.pi) / N
        for sigma in sigmas:
            for freq in freqs:
                filtered_real, filtered_img = gabor(img, freq, theta=theta, sigma_x=sigma, sigma_y=sigma, mode=mode,
                                                    cval=cval)
                pattern_features.append(filtered_real + np.complex(0, 1) * filtered_img)
    return pattern_features


# --------------------------------------------------


def halting_filter_pattern(raw_img, scribbled_img):
    freqs = get_frequencies(raw_img.shape)
    filter_bank_size = config.ORIENTATIONS * len(config.SIGMAS) * len(freqs)
    pattern_features = pattern_features_of_image_using_skimage(raw_img, config.ORIENTATIONS, config.SIGMAS, freqs,
                                                               mode='reflect')
    fvs_img = feature_vector_set_of_image(raw_img.shape, pattern_features, filter_bank_size,
                                          window_size=config.WINDOW_SIZE)
    fv_user = feature_vector_user(scribbled_img, fvs_img)
    d_map = distance_map(raw_img.shape, fvs_img, fv_user)
    hP = 1 / (1 + np.abs(d_map))
    return hP
