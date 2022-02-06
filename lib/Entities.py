#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5 import QtGui

from lib.Logger import Logger,FilePaths
from lib.PaintUtils import PaintUtils

import numpy as np
import json

class Entity(QWidget):
    def __init__(self,object_name):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.paint_utils = PaintUtils()
        
        self.config = {}
        self.path = None
        self.path_idx = 0
        self.path_idx_timer = QTimer()
        self.path_idx_timer.timeout.connect(self.increment_path_idx)
        self.load_config(object_name)
    
    def load_config(self,config_name):
        # Load the json config into a dictionary
        with open(f'{self.file_paths.entities_path}{config_name}.json','r') as fp:
            self.object_params = json.load(fp)
        self.config.update(self.object_params)

        # Convert pose to a numpy array
        x,y = self.config['pose']
        self.config['pose'] = np.array([x,y])

        # Generate a QPixmap from the png file
        png_name = f'{self.object_params["png_file"]}'
        self.pixmap = QtGui.QPixmap(f'{self.file_paths.entities_path}{png_name}')

        # Generate a QPen and QRect to display PNG border
        self.pen = QtGui.QPen()
        self.pen.setWidth(1)
        self.brush = QtGui.QBrush()
        self.brush.setStyle(Qt.NoBrush)
        self.pen.setColor(QtGui.QColor('black'))
        self.brush.setColor(QtGui.QColor('black'))
        self.bounding_size = np.array([self.pixmap.width(),self.pixmap.height()])

    def teleport(self,pose):
        '''
            Teleports the game object to the specified pose
            Params:
                pose (numpy.ndarray): A 1x2 array of ints specifying the position of an entity in screen pixels.
        '''
        if not isinstance(pose,np.ndarray):
            self.logger.log("Teleport pose must be a numpy array!",color='r')
            return
        self.config['pose'] = np.array(pose)

    def increment_path_idx(self):
        self.path_idx += 1
    
    def follow_path(self):
        if isinstance(self.path,np.ndarray):
            r,c = self.path.shape
            if self.path_idx == 0:
                x = self.path[0,self.path_idx]
                y = self.path[1,self.path_idx]
                self.config['pose'] = np.array([int(x),int(y)])
                if not self.path_idx_timer.isActive():
                    self.logger.log(f"Starting timer...")
                    self.path_idx_timer.start(500)
            elif self.path_idx < c:
                x = self.path[0,self.path_idx]
                y = self.path[1,self.path_idx]
                self.config['pose'] = np.array([int(x),int(y)])
                # self.path_idx += 1
            else:
                # self.path_idx = 0
                self.path_idx_timer.stop()

class Predator(Entity):
    def __init__(self,object_name):
        super().__init__(object_name)

    def update(self):
        self.follow_path()

class Prey(Entity):
    def __init__(self,object_name):
        super().__init__(object_name)
    
    def update(self):
        self.follow_path()

class Food(Entity):
    def __init__(self,object_name):
        super().__init__(object_name)
    
    def update(self):
        pass