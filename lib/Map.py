#!/usr/bin/env python3

from PyQt5 import QtGui

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger, FilePaths
from lib import Noise

import numpy as np
import os, json

class Tile():
    def __init__(self,pose,size,color,terrain_type,moisture):
        self.pose = pose
        self.size = size
        self.color = color
        self.terrain_type = terrain_type
        self.moisture_content = moisture

class Map(object):
    '''
    This class uses Perlin Noise to generate a 2D tile map.
    '''
    def __init__(self,x,y,idx=0):
        super().__init__()
        self.chunk_size = np.array([x,y])
        self.config = {'type':'map'}

        self.paint_utils = PaintUtils()
        self.logger = Logger()
        self.file_paths = FilePaths()

        self.map_config_idx = idx
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
                self.map_params[key]['noise'] = Noise.generate_fractal_noise_2d((self.chunk_size[0],self.chunk_size[1]),(1,1))
        self.map_configs = list(self.map_params.keys())
        self.logger.log(f'Map configs found: {self.map_configs}')
        
    def generate_map(self):
        tile_size = 30.0
        pose = np.array([0.0,0.0])
        size = np.array([tile_size,tile_size])
        color = None
        
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
                pose[1] += tile_size
            pose[1] = 0.0
            pose[0] += tile_size
