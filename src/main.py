from src.colorizer import *
from src.level_set_method import *

if __name__ == '__main__':
    np.seterr(divide='ignore', invalid='ignore')
    raw_img = cv2.cvtColor(cv2.imread(path.join(RAW_INPUT_FOLDER, 'wing.png')), cv2.COLOR_BGR2GRAY)
    scribbled_img = cv2.cvtColor(cv2.imread(path.join(SCRIBBLED_INPUT_FOLDER, 'wing.png')), cv2.COLOR_BGR2RGB)
    # phi = perform_LSM(raw_img, scribbled_img, 0.1, region=Region.intensity)

    # Pickle phi
    # pickle.dump(phi, open('phi', 'wb'))
    # phi = pickle.load(open('phi', 'rb'))

    # Create mask for colorization
    # phi[phi == 1] = 100
    # phi[phi <= 0] = 1
    # phi = np.ones_like(raw_img)
    # colored_img = strokePreservingColorization(raw_img, phi, np.array([255, 100, 100]).astype(np.float32))
    # plt.imshow(colored_img)
    # plt.show()

