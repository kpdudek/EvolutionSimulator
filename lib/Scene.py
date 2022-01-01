#!/usr/bin/env python3

from PyQt5 import QtCore, QtWidgets

from lib.Entities import Food, Predator,Prey
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
        self.map = None
        self.entities = {"food":{},"prey":{},"predators":{}}
        self.id = -1

    def initialize_scene(self,map_config_text,tile_size=30,size=(38,38),food_count=10,prey_count=10,predator_count=10):
        self.entities = {"food":{},"prey":{},"predators":{}}
        x,y = size
        self.logger.log(f'Creating map with chunk size: [{x},{y}] and tile size: {tile_size}')
        self.map = Map(x,y,tile_size=tile_size,config_text=map_config_text)

        self.astar = AStar(self.map)

        self.logger.log(f"Spawning {food_count} food, {prey_count} prey, and {predator_count} predator entities.")
        for idx in range(food_count):
            random_pose,idx = self.map.random_tile(invalid_tiles=['water','sand'])
            id_food = self.spawn_food('grass',random_pose)

        for idx in range(prey_count):
            random_pose,idx = self.map.random_tile()
            id_prey = self.spawn_prey('rabbit',random_pose)

        for idx in range(predator_count):
            random_pose,idx = self.map.random_tile()
            id = self.spawn_predator('wolf',random_pose)

        # s = self.map.tile_at(self.entities[id].config['pose'])
        # e = self.map.tile_at(self.entities[id_prey].config['pose'])
        # path,history = self.astar.get_plan(s,e)
        # self.entities[id].path = path

    def create_id(self):
        self.id += 1
        return self.id
    
    def spawn_food(self,object_type,pose):
        food = Food(object_type)
        food.teleport(pose)
        id = self.create_id()
        self.entities['food'].update({id:food})
        return id
    
    def spawn_predator(self,object_type,pose):
        pred = Predator(object_type)
        pred.teleport(pose)
        id = self.create_id()
        self.entities['predators'].update({id:pred})
        return id
    
    def spawn_prey(self,object_type,pose):
        prey = Prey(object_type)
        prey.teleport(pose)
        id = self.create_id()
        self.entities['prey'].update({id:prey})
        return id

    def update(self):
        pass
        # for entity in list(self.entities.values()):
            # entity.update()