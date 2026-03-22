from raylib import *
from pyray import *
import numpy as np
from enum import IntEnum
import math

SEED = 534543
TILE_SIZE = 16
LIGHT_GRAY = (175, 175, 175, 255)
DARK_GRAY = (25, 25, 25, 255)
WINDOW_WIDTH, WINDOW_HEIGHT = 960, 960

CHUNK_WIDTH, CHUNK_HEIGHT = 64, 64
WALL_THRESHOLD = 0.50
CHUNK_PADDING = 4
SMOOTHING_AMOUNT = 8
NEIGHBOUR_KERNEL = np.array([[1,1,1],
                                    [1,0,1],
                                    [1,1,1]], dtype=np.uint8)


class TileType(IntEnum):
    EMPTY = 0
    WALL = 1