from src.globals.constants import *

# general config
BRUSH_SIZE = 3
COLORIZATION_METHOD = Colorization.color_replacement
PHI_THRESHOLD = 0.0

# config for getting halting filter for intensity-continuous region
GAUSSIAN_SIGMA = 0.01

# config for getting halting filter for pattern-continuous region
CLUSTERS = 4
ORIENTATIONS = 6
GABOR_SIGMAS = (1, 3)
WINDOW_SIZE = 7

# config for level set method
CONTINUE_LSM = None
DISPLAY_STEP = 50
DT = 0.1
EPSILON = 5e-3
FA = 1
LEAK_PROOFING = True
LSM_THRESHOLD = 10
MAX_ITERATIONS = 10000
NR = 5
REGION = Region.intensity
RELAX_FACTOR = 0.4
START_PIXEL = None
