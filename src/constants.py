from os import path

THIS_FOLDER = path.dirname(path.abspath(__file__))
MEDIA_FOLDER = path.join(THIS_FOLDER, '../media/')
RAW_INPUT_FOLDER = path.join(MEDIA_FOLDER, 'raw/')
SCRIBBLED_INPUT_FOLDER = path.join(MEDIA_FOLDER, 'scribbled/')
OUTPUT_FOLDER = path.join(MEDIA_FOLDER, 'output/')
