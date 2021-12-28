#!/usr/bin/env python3

from PyQt5 import QtCore, QtWidgets

from lib.Logger import Logger, FilePaths
from lib.GameObjects import Predator,Prey
from lib.Map import Map

from numpy.ctypeslib import ndpointer
import numpy as np

class Scene(QtWidgets.QWidget):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,fps):
        super().__init__()
        self.logger = Logger()
        self.entities = {}
        self.initialize_scene()

    def initialize_scene(self):
        x,y = 64,34
        self.logger.log(f'Creating map with chunk size: [{x},{y}]')
        self.map = Map(x,y)
        self.entities.update({'map':self.map})
