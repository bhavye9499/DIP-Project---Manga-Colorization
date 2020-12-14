from src.constants import Region

# general config
FILENAME = None
REGION = Region.intensity

# config for getting halting filter for intensity-continuous region
SIGMA = 0.01

# config for getting halting filter for pattern-continuous region
ORIENTATIONS = 6
SIGMAS = (1, 3)
WINDOW_SIZE = 7

# config for level set method
CONTINUE_LSM = None
DT = 0.1
EPSILON = 5e-3
FA = 1
DISPLAY_STEP = 50
LSM_THRESHOLD = 10
NR = 5
RELAX_FACTOR = 0.4
