import cv2
import numpy as np
import math

from skimage.filters import gabor_kernel


def generate_filter_bank(M, N, p, q, fmax=0.25, gama=math.sqrt(2), eta=math.sqrt(2)):
    """
    M	:	No. of scales (usually set to 5)
    N	:	No. of orientations (usually set to 8)
    p	:	No. of rows in a 2-D Gabor filter (an odd integer number, usually set to 39)
    q	:	No. of columns in a 2-D Gabor filter (an odd integer number, usually set to 39)
    """
    filter_bank = []
    for i in range(M):
        fu = fmax / (math.sqrt(2) ** i)
        alpha = fu / gama
        beta = fu / eta
        for j in range(N):
            tetav = (j / N) * math.pi
            filter = np.zeros((p, q), dtype=np.complex_)
            for x in range(p):
                for y in range(q):
                    xprime = (x - (p // 2)) * math.cos(tetav) + (y - (q // 2)) * math.sin(tetav)
                    yprime = -(x - (p // 2)) * math.sin(tetav) + (y - (q // 2)) * math.cos(tetav)
                    filter[x, y] = ((fu ** 2) / (math.pi * gama * eta) *
                                    np.exp(-((alpha ** 2) * (xprime ** 2) + (beta ** 2) * (yprime ** 2))) *
                                    np.exp(np.complex(0, 1) * 2 * math.pi * fu * xprime))
            filter_bank.append(filter)
    return filter_bank


def generate_filter_bank_using_opencv(M, N, p, q, sigma=np.pi, gamma=0.5, phi=0):
    """
    M	:	No. of scales (usually set to 5)
    N	:	No. of orientations (usually set to 8)
    p	:	No. of rows in a 2-D Gabor filter (an odd integer number, usually set to 39)
    q	:	No. of columns in a 2-D Gabor filter (an odd integer number, usually set to 39)
    Create gabor filter bank using getGaborKernel() method in cv2 package
    """
    filter_bank = []
    for n in range(N):
        for m in range(M):
            theta = (n * np.pi) / N
            lamda = (m + 1) * np.pi
            kernel = cv2.getGaborKernel((p, q), sigma, theta, lamda, gamma, phi, ktype=cv2.CV_32F)
            filter_bank.append(kernel)
    return filter_bank


def generate_filter_bank_using_skimage(N, sigmas=(1, 3), freqs=(0.5, 0.25)):
    """
    N	:	No. of orientations (usually set to 8)
    Create gabor filter bank using gabor_kernel method in skimage package
    """
    filter_bank = []
    for n in range(N):
        theta = (n * np.pi) / N
        for sigma in sigmas:
            for freq in freqs:
                kernel = np.real(gabor_kernel(freq, theta=theta, sigma_x=sigma, sigma_y=sigma))
                filter_bank.append(kernel)
    return filter_bank
