#!/usr/bin/env python3

from PyQt5 import QtCore, QtWidgets

from lib.Logger import Logger, FilePaths
from lib.GameObjects import Predator,Prey
from lib.Map import Map

from numpy.ctypeslib import ndpointer
from random import randint
import numpy as np

class Scene(QtWidgets.QWidget):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,fps):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.entities = {}

    def initialize_scene(self,map_config_text,tile_size=30,size=(38,38)):
        x,y = size
        self.logger.log(f'Creating map with chunk size: [{x},{y}]')
        self.map = Map(x,y,tile_size=tile_size,config_text=map_config_text)
        self.entities.update({'map':self.map})

        random_pose = np.array([randint(0,x)*tile_size,randint(0,y)*tile_size])
        rabbit = Prey('rabbit')
        rabbit.teleport(random_pose)
        self.entities.update({'rab1':rabbit})

        random_pose = np.array([randint(0,x)*tile_size,randint(0,y)*tile_size])
        wolf = Predator('wolf')
        wolf.teleport(random_pose)
        self.entities.update({'wol1':wolf})
