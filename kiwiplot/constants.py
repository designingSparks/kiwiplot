import os
# BASEDIR = os.path.abspath('.')
BASEDIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(BASEDIR, 'images')

from enum import Enum, auto
class ZOOM_MODE(Enum):
    freeZoom = auto()
    xZoom = auto()
    yZoom = auto()
