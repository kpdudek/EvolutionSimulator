#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5 import QtGui, uic

from lib.Logger import FilePaths, Logger
from lib.Map import Map

import numpy as np

class SimulationController(QWidget):
    '''
    This class initializes the window
    '''
    shutdown_signal = pyqtSignal()

    def __init__(self,scene,camera):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.scene = scene
        self.camera = camera

        uic.loadUi(f'{self.file_paths.user_path}ui/simulation_controller.ui',self)
        self.setWindowTitle('Simulation Controller')

        self.create_button.clicked.connect(self.set_map_config)
        self.update_map_configs_combobox()

        self.apply_settings()
        self.show()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.logger.log(f'Sending shutdown signal...')
            self.shutdown_signal.emit()
        elif key == Qt.Key_1:
            self.close()
    
    def apply_settings(self):
        self.set_map_config()

    def set_map_config(self):
        idx = self.map_config_combobox.currentIndex()
        self.logger.log(f'Setting map index: {idx}')

        x = self.x_map_size_spinbox.value()
        y = self.y_map_size_spinbox.value()
        self.scene.map = Map(x,y,idx)
        self.scene.entities['map'] = self.scene.map

    def update_map_configs_combobox(self):
        self.map_config_combobox.addItems(self.scene.map.map_configs)
