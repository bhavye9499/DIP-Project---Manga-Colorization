from src.constants import *
from src.level_set_method import *

if __name__ == '__main__':
    np.seterr(divide='ignore', invalid='ignore')
    raw_img = cv2.cvtColor(cv2.imread(path.join(RAW_INPUT_FOLDER, 'wing.png')), cv2.COLOR_BGR2GRAY)
    scribbled_img = cv2.imread(path.join(SCRIBBLED_INPUT_FOLDER, 'wing.png'))
    phi = perform_LSM(raw_img, scribbled_img, 0.1, region=Region.intensity, leak_proofing=True)
