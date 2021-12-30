#!/usr/bin/env python3

from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QWidget

from lib.Logger import Logger,FilePaths
from lib.PaintUtils import PaintUtils

import numpy as np
import os,json,random

class Entity(QWidget):
    def __init__(self,object_name):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.paint_utils = PaintUtils()
        
        self.config = {}
        self.load_config(object_name)
    
    def load_config(self,config_name):
        with open(f'{self.file_paths.game_objects_path}{config_name}.json','r') as fp:
            self.object_params = json.load(fp)
        self.config.update(self.object_params)
        png_name = f'{self.object_params["object"]}.png'
        self.pixmap = QtGui.QPixmap(f'{self.file_paths.game_objects_path}{png_name}')

    def teleport(self,x,y):
        self.config.pose = [x,y]

class Predator(Entity):
    def __init__(self,object_name):
        super().__init__(object_name)

class Prey(Entity):
    def __init__(self,object_name):
        super().__init__(object_name)

class Food(Entity):
    def __init__(self,object_name):
        super().__init__(object_name)