#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget

from lib.Logger import Logger,FilePaths

import numpy as np

class Entity(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()

class Predator(Entity):
    def __init__(self):
        super().__init__()

class Prey(Entity):
    def __init__(self):
        super().__init__()