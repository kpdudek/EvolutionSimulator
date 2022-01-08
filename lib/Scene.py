#!/usr/bin/env python3

from random import randint
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
            while not isinstance(self.map.tiles[idx].entity,type(None)):
                random_pose,idx = self.map.random_tile(invalid_tiles=['water','sand'])
            id_food = self.spawn_food('grass',random_pose)
            self.map.tiles[idx].entity = self.entities['food'][id_food]

        for idx in range(prey_count):
            random_pose,idx = self.map.random_tile()
            while not isinstance(self.map.tiles[idx].entity,type(None)):
                random_pose,idx = self.map.random_tile()
            id_prey = self.spawn_prey('rabbit',random_pose)
            self.map.tiles[idx].entity = self.entities['prey'][id_prey]

        for idx in range(predator_count):
            random_pose,idx = self.map.random_tile()
            while not isinstance(self.map.tiles[idx].entity,type(None)):
                random_pose,idx = self.map.random_tile()
            id = self.spawn_predator('wolf',random_pose)
            self.map.tiles[idx].entity = self.entities['predators'][id]

    def create_id(self):
        self.id += 1
        return self.id
    
    def spawn_food(self,object_type,pose):
        food = Food(object_type)
        food.teleport(pose)
        id = self.create_id()
        name = f'food{id}'
        self.entities['food'].update({name:food})
        return name
    
    def spawn_predator(self,object_type,pose):
        pred = Predator(object_type)
        pred.teleport(pose)
        id = self.create_id()
        name = f'predator{id}'
        self.entities['predators'].update({name:pred})
        return name
    
    def spawn_prey(self,object_type,pose):
        prey = Prey(object_type)
        prey.teleport(pose)
        id = self.create_id()
        name = f'prey{id}'
        self.entities['prey'].update({name:prey})
        return name

    def update(self):
        for key,entity_type in self.entities.items():
            if key != 'food':
                for key,entity in entity_type.items():
                    if isinstance(entity.path,type(None)):
                        s = self.map.tile_at(entity.config['pose'])
                        if entity.config['type']=='predator':
                            prey = list(self.entities['prey'].keys())
                            idx = randint(0,len(prey)-1)
                            e = self.map.tile_at(self.entities['prey'][prey[idx]].config['pose'])
                            self.logger.log(f'{key} requested a path to {prey[idx]}')
                        elif entity.config['type']=='prey':
                            food = list(self.entities['food'].keys())
                            idx = randint(0,len(food)-1)
                            e = self.map.tile_at(self.entities['food'][food[idx]].config['pose'])
                            self.logger.log(f'{key} requested a path to {food[idx]}')
                        self.astar.clear_search()
                        entity.path,history = self.astar.get_plan(key,s,e)
                    entity.update()