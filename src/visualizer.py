import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import TruncatedSVD
from PIL import Image


def visualize_distance_map(distance_map, cmap=None):
    plt.imshow(distance_map, cmap=cmap)
    plt.colorbar()
    plt.show()


def visualize_feature_vectors(feature_vectors):
    model = TruncatedSVD(n_components=2)
    svd_data = model.fit_transform(feature_vectors)
    plt.scatter(svd_data[:, 0], svd_data[:, 1])
    plt.show()


def visualize_filter_bank(filter_bank, m, n):
    fig, axs = plt.subplots(m, n)
    for i in range(m):
        for j in range(n):
            if m == 1:
                axs[j].imshow(np.real(filter_bank[i * m + j]), cmap='gray')
            else:
                axs[i, j].imshow(np.real(filter_bank[i * n + j]), cmap='gray')
    plt.show()


def visualize_image(img_arr):
    Image.fromarray(img_arr).show()
