#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtGui, uic

from lib.Logger import FilePaths, Logger

import numpy as np

class SimulationController(QWidget):
    '''
    This class initializes the window
    '''
    def __init__(self,scene,camera):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.scene = scene
        self.camera = camera

        uic.loadUi(f'{self.file_paths.user_path}ui/simulation_controller.ui',self)
        self.setWindowTitle('Simulation Controller')

        # self.map_config_combobox.currentIndexChanged.connect(self.set_map_config)
        self.apply_button.clicked.connect(self.set_map_config)
        self.update_map_configs_combobox()

        self.apply_settings()
        self.show()
    
    def apply_settings(self):
        pass

    def set_map_config(self,i):
        idx = self.map_config_combobox.currentIndex()
        self.logger.log(f'Setting map index: {idx}')
        self.scene.map.map_config_idx = idx
        self.scene.map.generate_map()

    def update_map_configs_combobox(self):
        self.map_config_combobox.addItems(self.scene.map.map_configs)
