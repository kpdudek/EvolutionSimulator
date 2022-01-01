#!/usr/bin/env python3

from PyQt5 import QtCore, QtWidgets

from lib.GameObjects import Food, Predator,Prey
from lib.Logger import Logger, FilePaths
from lib.AStar import AStar
from lib.Map import Map

import numpy as np

class Scene(QtWidgets.QWidget):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,fps):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.id = -1
        self.entities = {}

    def initialize_scene(self,map_config_text,tile_size=30,size=(38,38)):
        self.entities = {}
        x,y = size
        self.logger.log(f'Creating map with chunk size: [{x},{y}]')
        self.map = Map(x,y,tile_size=tile_size,config_text=map_config_text)

        random_pose,idx = self.map.random_tile()
        id_prey = self.spawn_prey('rabbit',random_pose)

        random_pose,idx = self.map.random_tile()
        id = self.spawn_predator('wolf',random_pose)
        self.entities[id].hunting = self.entities[id_prey]

        self.astar = AStar(self.map)
        s = self.map.tile_at(self.entities[id].config['pose'])
        e = self.map.tile_at(self.entities[id_prey].config['pose'])
        path,history = self.astar.get_plan(s,e)
        self.entities[id].path = path

    def create_id(self):
        self.id += 1
        return self.id
    
    def spawn_food(self,object_type,pose):
        food = Food(object_type)
        food.teleport(pose)
        id = self.create_id()
        self.entities.update({id:food})
        return id
    
    def spawn_predator(self,object_type,pose):
        pred = Predator(object_type)
        pred.teleport(pose)
        id = self.create_id()
        self.entities.update({id:pred})
        return id
    
    def spawn_prey(self,object_type,pose):
        prey = Prey(object_type)
        prey.teleport(pose)
        id = self.create_id()
        self.entities.update({id:prey})
        return id

    def update(self):
        for entity in list(self.entities.values()):
            pass