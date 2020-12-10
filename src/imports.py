import cv2
import enum
import math
import numpy as np
import pickle
import random

from matplotlib import pyplot as plt
from os import path, pardir
from PIL import Image
from scipy import ndimage as ndi
from skimage.color import label2rgb
from skimage.filters import gabor
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.decomposition import TruncatedSVD
from tqdm import tqdm
