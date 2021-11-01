import os
BASEDIR = os.path.abspath('.')
IMAGE_DIR = os.path.join(BASEDIR, 'images')




# ## zoom modes
# ZOOM_MODE = {
#     'freeZoom': 0,
#     'xZoom': 1,
#     'yZoom' :2
# }

from enum import Enum, auto
class ZOOM_MODE(Enum):
    freeZoom = auto()
    xZoom = auto()
    yZoom = auto()
