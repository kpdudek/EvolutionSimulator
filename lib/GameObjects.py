#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget

from lib.Logger import Logger,FilePaths
from lib.PaintUtils import PaintUtils

import numpy as np
import os,json

class Entity(QWidget):
    def __init__(self,object_name):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.paint_utils = PaintUtils()

        self.config = {}
        self.load_config(object_name)

class Predator(Entity):
    def __init__(self):
        super().__init__()

class Prey(Entity):
    def __init__(self):
        super().__init__()