from src.visualizer import *
from src.imports import *


def get_frequencies(shape):
    numRows = shape[0]
    numCols = shape[1]
    wavelengthMin = 4 / np.sqrt(2)
    wavelengthMax = np.hypot(numRows, numCols)
    n = np.floor(np.log2(wavelengthMax / wavelengthMin))
    wavelength = np.power(2, np.arange(0, n - 1, 1)) * wavelengthMin
    return 1 / wavelength


def get_pixel_neighbourhood(mat, location, shape):
    x, y = location
    P, Q = shape
    x_max = min(x + P // 2, mat.shape[0])
    y_max = min(y + Q // 2, mat.shape[1])
    x_min = max(x - P // 2, 0)
    y_min = max(y - Q // 2, 0)
    return mat[x_min:x_max, y_min:y_max]


def get_major_cluster(feature_vectors, eps=1, min_samples=20):
    model = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    yhat = model.fit_predict(feature_vectors)
    clusters, cluster_counts = np.unique(yhat, return_counts=True)
    print(f'clusters = {list(zip(clusters, cluster_counts))}')
    visualize_clustered_feature_vectors(feature_vectors, yhat)
    M_cluster_counts = max(cluster_counts[1:] if clusters[0] == -1 else cluster_counts)
    M_cluster = clusters[np.where(cluster_counts == M_cluster_counts)[0][0]]
    row_ix = np.where(yhat == M_cluster)
    major_cluster = np.asarray(feature_vectors)[row_ix]
    return major_cluster


def get_scribbled_pixels(scribbled_img, delta=10):
    P, Q, _ = scribbled_img.shape
    scribbled_pixels = []
    for y in range(P):
        for x in range(Q):
            pixel = scribbled_img[y, x]
            if max(pixel) - min(pixel) > delta:
                scribbled_pixels.append((x, y))
    return scribbled_pixels


def grad2d(f):
    return np.gradient(f)


def log_transform(f):
    c = 255 / math.log(1 + np.max(f))
    return c * np.log(1 + f)


def mag_grad2d(fx, fy):
    mag_grad_f = np.sqrt(np.square(fx) + np.square(fy))
    return mag_grad_f


def map_mat(mat, mn=0, mx=1):
    """
    Map the range of matrix to mn-mx.
    :param mat: matrix
    :param mn: min
    :param mx: max
    :return: mapped matrix
    """
    mat_mn = mat.min()
    mat_mx = mat.max()
    return mn + ((mat - mat_mn) / (mat_mx - mat_mn)) * (mx - mn)


def normalize_and_scale(f):
    f_new = f - np.min(f)
    return (f_new / np.max(f_new)) * 255
