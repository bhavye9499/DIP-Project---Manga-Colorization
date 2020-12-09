from src.generic_imports import *

THIS_FOLDER = path.dirname(path.abspath(__file__))
MEDIA_FOLDER = path.join(THIS_FOLDER, pardir, 'media')
RAW_INPUT_FOLDER = path.join(MEDIA_FOLDER, 'raw')
SCRIBBLED_INPUT_FOLDER = path.join(MEDIA_FOLDER, 'scribbled')
OUTPUT_FOLDER = path.join(MEDIA_FOLDER, 'output')

ORIENTATIONS = 6
SIGMAS = (1, 3)
FREQS = (0.05, 0.25)

NR = 1
EPSILON = 5e-3
FA = 1
RELAX_FACTOR = 0.4
