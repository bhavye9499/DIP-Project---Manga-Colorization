from src.constants import *
from src.distance_map import *
from src.feature_vector import *
from src.filter_bank import *
from src.generic_imports import *
from src.halting_filter import *
from src.level_set_method import *
from src.pattern_feature import *
from src.visualizer import *

if __name__ == '__main__':
    raw_img = cv2.cvtColor(cv2.imread(path.join(RAW_INPUT_FOLDER, 'test3.jpg')), cv2.COLOR_BGR2GRAY).astype(np.float_)
    scribbled_img = cv2.imread(path.join(SCRIBBLED_INPUT_FOLDER, 'test3-1.jpg')).astype(np.float_)
    # visualize_image(raw_img)
    # visualize_image(scribbled_img, mode='RGB')

    # phi = get_initial_phi(scribbled_img)
    # hI = get_halting_filter_intensity(raw_img)
    phi = perform_LSM(raw_img, scribbled_img, 1, 500, leak_proofing=False)

    # filter_bank_size = orientations * len(sigmas) * len(freqs)
    # filter_bank = generate_filter_bank(4, 6, 3, 3)
    # filter_bank = generate_filter_bank_using_skimage(6, sigmas, freqs)
    # visualize_filter_bank(filter_bank, 6, 4)

    # pattern_features = pattern_features_of_image_from_filter_bank(raw_img, filter_bank)
    # pattern_features = pattern_features_of_image_using_skimage(raw_img, orientations, sigmas, freqs, mode='reflect')

    # fvs_img = feature_vector_set_of_image(raw_img.shape, pattern_features, filter_bank_size, window_size=7)
    # visualize_feature_vector_set_of_image(fvs_img, n_clusters=4)

    # fv_user = feature_vector_user(scribbled_img, fvs_img)

    # d_map = distance_map(raw_img.shape, fvs_img, fv_user)
    # visualize_distance_map(d_map, cmap='viridis')
