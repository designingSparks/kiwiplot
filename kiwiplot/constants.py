import os
# BASEDIR = os.path.abspath('.')
BASEDIR = os.path.dirname(os.path.realpath(__file__))
IMAGE_DIR = os.path.join(BASEDIR, 'images')

#Cursor anchors
HLINE_TOP = (0.5, 0)
HLINE_BOT = (0.5, 1)
VLINE_LEFT = (0, 0.5)
VLINE_RIGHT = (1, 0.5)

from enum import Enum, auto
class ZOOM_MODE(Enum):
    freeZoom = auto()
    xZoom = auto()
    yZoom = auto()
