#!/usr/bin/env python3

from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from numpy.core.numeric import ones

from lib.Logger import Logger, FilePaths
from lib.PaintUtils import PaintUtils
import lib.Errors as errors
from lib import Noise

from random import randint
import numpy as np
import math, json

class Tile():
    def __init__(self,pose,size,color,terrain_type,moisture,sunlight):
        self.pose = pose
        self.size = size
        if not isinstance(color,QtGui.QColor):
            raise errors.MustBeQColor(color)
        self.color = color
        self.terrain_type = terrain_type
        self.moisture_content = moisture
        self.sunlight = sunlight
        self.entity = None

        # Pen and Brush for the camera to use
        self.pen = QtGui.QPen()
        self.pen.setWidth(1)
        self.brush = QtGui.QBrush()
        self.brush.setStyle(Qt.SolidPattern)
        self.pen.setColor(self.color)
        self.brush.setColor(self.color)

        # Roadmap data
        self.neighbors = []
        self.neighbors_cost = []
        self.backpointer = None
        self.backpointer_cost = None

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
        self.tiles = np.empty([x,y],dtype=Tile)

        self.load_config()
        self.generate_map()
        self.set_neighbors()

    def load_config(self):
        with open(f'{self.file_paths.maps_path}configs.json','r') as fp:
            self.map_params = json.load(fp)

        # Get the name of the map config (which is one of the dict keys) based on the passed index or object name.
        self.map_config_names = list(self.map_params.keys())
        if self.map_config_text:
            self.config_name = self.map_config_text
        else:
            self.config_name = self.map_config_names[self.map_config_idx]

        # Generate the height map based on which type of noise that map config uses.
        if self.map_params[self.config_name]['type'] == 'perlin':
            self.map_params[self.config_name]['noise'] = Noise.generate_perlin_noise(self.chunk_size[0],self.chunk_size[1])
        elif self.map_params[self.config_name]['type'] == 'fractal':
            self.map_params[self.config_name]['noise'] = Noise.generate_fractal_noise_2d((self.chunk_size[0],self.chunk_size[1]),(2,2))
        elif self.map_params[self.config_name]['type'] == 'none':
            self.map_params[self.config_name]['noise'] = np.ones((self.chunk_size[0],self.chunk_size[1]))
        
    def generate_map(self):
        pose = np.array([0.0,0.0])
        size = np.array([self.tile_size,self.tile_size])
        color = None
        
        noise = self.map_params[self.config_name]['noise']
        land_cutoff = self.map_params[self.config_name]['land_cutoff']
        sand_cutoff = self.map_params[self.config_name]['sand_cutoff']
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
                sunlight = 1.0
                tile = Tile(pose.copy(),size.copy(),color,terrain_type,moisture,sunlight)
                self.tiles[x,y] = tile
                pose[1] += self.tile_size
            pose[1] = 0.0
            pose[0] += self.tile_size
        
        self.pix_size = np.array([self.chunk_size[0]*self.tile_size,self.chunk_size[1]*self.tile_size])

    def set_neighbors(self,invalid_terrain=['water']):
        # For every tile in the map
        for r in range(self.chunk_size[0]):
            for c in range(self.chunk_size[1]):

                # For every neighbor of that tile, diagonals included
                for nx in range(-1,2):
                    for ny in range(-1,2):
                
                        # Ignore the current tile (r,c), when both offsets are zero
                        if nx == 0 and ny == 0:
                            pass
                        # Check if the offsets are in the bounds of the map (0 < idx < chunk size)
                        elif r+nx >= 0 and r+nx < self.chunk_size[0] and c+ny >= 0 and c+ny < self.chunk_size[1]:
                            if self.tiles[r+nx,c+ny].terrain_type not in invalid_terrain:
                                self.tiles[r,c].neighbors.append((r+nx,c+ny))
                                if abs(nx) == 1 and abs(ny) == 1:
                                    self.tiles[r,c].neighbors_cost.append(math.pow(math.pow(self.tile_size,2)+math.pow(self.tile_size,2),0.5))
                                else:
                                    self.tiles[r,c].neighbors_cost.append(self.tile_size)

    def tile_at(self,coord):
        '''
            Accepts a coordinate in world space and returns the corresponding tile index
            Params:
                coord (numpy.ndarray): A 1x2 numpy array of ints corresponding to screen coordinates in pixel space.
            Returns:
                tile_presss (numpy.ndarray): A 1x2 numpy array of ints corresponding to tile index coordinates in range [0,chunk_size]
        '''
        x = math.floor(coord[0]/self.tile_size)
        y = math.floor(coord[1]/self.tile_size)
        if x < self.chunk_size[0] and x >= 0 and y < self.chunk_size[1] and y >= 0:
            return (x,y)
        else:
            return None

    def random_tile(self,invalid_tiles=['water']):
        '''
            Get a random tile in the map.
        '''
        x = randint(0,self.chunk_size[0]-1)
        y = randint(0,self.chunk_size[1]-1)
        while self.tiles[x,y].terrain_type in invalid_tiles:
            x = randint(0,self.chunk_size[0]-1)
            y = randint(0,self.chunk_size[1]-1)
        random_pose = np.array([x*self.tile_size,y*self.tile_size])
        return random_pose,(x,y)

    def tile_borders_visible(self,bool):
        for row in self.tiles:
            for tile in row:
                if bool:
                    tile.pen.setColor(QtGui.QColor('black'))
                else:
                    tile.pen.setColor(tile.color)