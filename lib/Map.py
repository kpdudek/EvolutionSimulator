#!/usr/bin/env python3

from PyQt5 import QtGui

from lib.Logger import Logger
from lib import Noise

import numpy as np

from lib.PaintUtils import PaintUtils

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
    def __init__(self,x,y):
        super().__init__()
        self.chunk_size = np.array([x,y])
        self.config = {'type':'map'}

        self.paint_utils = PaintUtils()
        self.logger = Logger()

        self.tiles = []
        self.generate_map()

    def generate_map(self):
        tile_size = 30.0
        pose = np.array([0.0,0.0])
        size = np.array([tile_size,tile_size])
        color = None
        
        # noise = Noise.generate_perlin_noise(self.chunk_size[0],self.chunk_size[1])
        # noise = Noise.generate_fractal_noise_2d((self.chunk_size[0],self.chunk_size[1]),(1,1))

        map_params = {
                    "perlin":{
                                "noise":Noise.generate_perlin_noise(self.chunk_size[0],self.chunk_size[1]),
                                "land_cutoff":0.0,
                                "sand_cutoff":-0.15},
                    "fractal":{
                                "noise":Noise.generate_fractal_noise_2d((self.chunk_size[0],self.chunk_size[1]),(1,1)),
                                "land_cutoff":-0.08,
                                "sand_cutoff":-0.11}}
        
        map_configs = list(map_params.keys())
        self.logger.log(f'Map configs found: {map_configs}')
        noise_type = map_configs[1]
        noise = map_params[noise_type]['noise']
        land_cutoff = map_params[noise_type]['land_cutoff']
        sand_cutoff = map_params[noise_type]['sand_cutoff']
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
