from src.constants import *
from src.distance_map import *
from src.feature_vector import *
from src.filter_bank import *
from src.pattern_feature import *
from src.visualizer import *

if __name__ == '__main__':
    raw_img = cv2.cvtColor(cv2.imread(path.join(RAW_INPUT_FOLDER, 'tree.jpg')), cv2.COLOR_BGR2GRAY)
    scribbled_img = cv2.imread(path.join(SCRIBBLED_INPUT_FOLDER, 'tree.jpg'))

    filter_bank = generate_filter_bank(4, 6, 5, 5)
    # visualize_filter_bank(filter_bank, 4, 6)

    pattern_features = pattern_features_of_image(raw_img, filter_bank)

    fv_user = feature_vector_user(raw_img, scribbled_img, pattern_features, filter_bank)

    d_map = distance_map(raw_img.shape, pattern_features, filter_bank, fv_user)
    visualize_distance_map(d_map, cmap='viridis')
