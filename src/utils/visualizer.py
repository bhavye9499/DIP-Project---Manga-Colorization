import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from sklearn.decomposition import TruncatedSVD

from src.utils import utils


def visualize_clustered_feature_vectors(feature_vectors, cluster_ids):
    model = TruncatedSVD(n_components=2)
    yhat = model.fit_transform(feature_vectors)
    clusters = np.unique(cluster_ids)
    for cluster in clusters:
        row_ix = np.where(cluster_ids == cluster)
        plt.scatter(yhat[row_ix, 0], yhat[row_ix, 1])
    plt.legend(labels=[f'Cluster_{cluster}' for cluster in clusters])
    plt.show()


def visualize_distance_map(distance_map, cmap=None):
    plt.imshow(distance_map, cmap=cmap)
    plt.colorbar()
    plt.show()


def visualize_feature_vectors(feature_vectors):
    model = TruncatedSVD(n_components=2)
    yhat = model.fit_transform(feature_vectors)
    plt.scatter(yhat[:, 0], yhat[:, 1])
    plt.show()


def visualize_image_feature_vectors(img_fvs, n_clusters, cmap=None):
    output = utils.perform_clustering(img_fvs, n_clusters)
    plt.imshow(output, cmap=cmap)
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


def visualize_halting_filter_intensity(hI):
    plt.imshow(utils.log_transform(hI), cmap='gray')
    plt.show()
    plt.imshow(utils.log_transform(hI), cmap='gray')
    plt.show()


def visualize_halting_filter_pattern(hP):
    plt.imshow(hP, cmap='gray')
    plt.show()


def visualize_image(img_arr, mode=None):
    Image.fromarray(img_arr, mode=mode).show()


def visualize_scribbled_pixels(img, scribbled_pixels):
    output = img
    for x, y in scribbled_pixels:
        output[x, y] = 0
    plt.imshow(output, cmap='gray')
    plt.show()
