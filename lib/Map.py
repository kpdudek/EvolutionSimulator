#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from lib.Logger import Logger, FilePaths
from lib.PaintUtils import PaintUtils
import lib.Errors as errors
from lib import Noise

import numpy as np
import os, json

class Tile():
    def __init__(self,pose,size,color,terrain_type,moisture):
        self.pose = pose
        self.size = size
        if not isinstance(color,QtGui.QColor):
            raise errors.MustBeQColor(color)
        self.color = color
        self.terrain_type = terrain_type
        self.moisture_content = moisture

        self.pen = QtGui.QPen()
        self.pen.setWidth(1)
        self.brush = QtGui.QBrush()
        self.brush.setStyle(Qt.SolidPattern)

        self.pen.setColor(self.color)
        self.brush.setColor(self.color)

class Map(object):
    '''
    This class uses Perlin Noise to generate a 2D tile map.
    '''
    def __init__(self,x,y,tile_size=30,config_text=None,idx=0):
        super().__init__()
        self.chunk_size = np.array([x,y])
        self.config = {'type':'map'}

        self.paint_utils = PaintUtils()
        self.logger = Logger()
        self.file_paths = FilePaths()

        self.map_config_idx = idx
        self.map_config_text = config_text
        self.tile_size = tile_size
        self.tiles = []
        self.load_configs()
        self.generate_map()

    def load_configs(self):
        fp = open(f'{self.file_paths.maps_path}configs.json','r')
        self.map_params = json.load(fp)
        fp.close()
        keys = list(self.map_params.keys())
        for key in keys:
            if self.map_params[key]['type'] == 'perlin':
                self.map_params[key]['noise'] = Noise.generate_perlin_noise(self.chunk_size[0],self.chunk_size[1])
            elif self.map_params[key]['type'] == 'fractal':
                self.map_params[key]['noise'] = Noise.generate_fractal_noise_2d((self.chunk_size[0],self.chunk_size[1]),(2,2))
        self.map_configs = list(self.map_params.keys())
        self.logger.log(f'Map configs found: {self.map_configs}')
        
    def generate_map(self):
        pose = np.array([0.0,0.0])
        size = np.array([self.tile_size,self.tile_size])
        color = None
        
        if self.map_config_text:
            noise_type = self.map_config_text
        else:
            noise_type = self.map_configs[self.map_config_idx]
        noise = self.map_params[noise_type]['noise']
        land_cutoff = self.map_params[noise_type]['land_cutoff']
        sand_cutoff = self.map_params[noise_type]['sand_cutoff']
        for x in range(self.chunk_size[0]):
            for y in range(self.chunk_size[1]):
                if noise[x,y] >= land_cutoff:
                    color = QtGui.QColor(self.paint_utils.colors['grass_green'])
                    terrain_type = 'grass'
                    moisture = .3
                elif noise[x,y] >= sand_cutoff:
                    color = QtGui.QColor(self.paint_utils.colors['sand'])
                    terrain_type = 'sand'
                    moisture = .6
                elif noise[x,y] < sand_cutoff:
                    color = QtGui.QColor(self.paint_utils.colors['water_blue'])
                    terrain_type = 'water'
                    moisture = 1.0
                tile = Tile(pose.copy(),size.copy(),color,terrain_type,moisture)
                self.tiles.append(tile)
                pose[1] += self.tile_size
            pose[1] = 0.0
            pose[0] += self.tile_size
