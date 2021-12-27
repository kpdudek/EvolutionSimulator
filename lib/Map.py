#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui

from lib.Logger import Logger
from lib.Noise import generate_perlin_noise

import numpy as np
import time

from lib.PaintUtils import PaintUtils

class Tile():
    def __init__(self,pose,size,color):
        self.pose = pose
        self.size = size
        self.color = color

class Map(object):
    '''
    This class uses Perlin Noise to generate a 2D tile map.
    '''
    def __init__(self,x,y):
        super().__init__()
        self.chunk_size = np.array([x,y])
        self.config = {'type':'map'}

        self.paint_utils = PaintUtils()

        self.tiles = []
        self.generate_map()

    def generate_map(self):
        tile_size = 30.0
        pose = np.array([0.0,0.0])
        size = np.array([tile_size,tile_size])
        color = None
        
        noise = generate_perlin_noise(self.chunk_size[0],self.chunk_size[1])
        for x in range(self.chunk_size[0]):
            for y in range(self.chunk_size[1]):
                # color = self.paint_utils.random_color()
                color = QtGui.QColor(0,0,0,noise[x,y]*255)
                tile = Tile(pose.copy(),size.copy(),color)
                self.tiles.append(tile)
                pose[1] += tile_size
            pose[1] = 0.0
            pose[0] += tile_size
