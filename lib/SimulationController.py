#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5 import QtGui, uic

from lib.Logger import FilePaths, Logger
from lib.Map import Map

import numpy as np

class SimulationController(QMainWindow):
    '''
    This class initializes the window
    '''
    shutdown_signal = pyqtSignal()

    def __init__(self,canvas):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.canvas = canvas
        self.is_shutting_down = False

        uic.loadUi(f'{self.file_paths.user_path}ui/simulation_controller_mainwindow.ui',self)
        self.setWindowTitle('Simulation Controller')

        self.create_button.clicked.connect(self.apply_settings)
        self.action_save_default.triggered.connect(self.save_as_default)
        self.action_load_default.triggered.connect(self.load_default)

        self.apply_settings()
        self.update_map_configs_combobox()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.logger.log(f'Sending shutdown signal...')
            self.shutdown_signal.emit()
        elif key == Qt.Key_1:
            self.close()

    def showEvent(self, e):
        self.logger.log('Open signal received.')
        self.is_shutting_down = False

    def closeEvent(self, e):
        if not self.is_shutting_down:
            self.logger.log('Shutdown signal received.')
            self.is_shutting_down = True
        self.shutdown()
    
    def shutdown(self):
        self.close()

    def save_as_default(self):
        self.logger.log(f'Saving current simulation as default...')

    def load_default(self):
        self.logger.log(f'Loading default simulation...')

    def update_map_configs_combobox(self):
        self.map_config_combobox.addItems(self.canvas.scene.map.map_configs)

    def apply_settings(self):
        '''
            Generate a new simulation by calling each settings method
        '''
        self.set_map_config()
        self.set_fps_logging()
        self.set_fps_display()

    ####################################################################################################
    #   Settings Methods:
    #       The following methods implement the actions needed to generate a new simulation.
    #       The apply_settings() method calls each of these methods to generate a new simulation.
    ####################################################################################################
    def set_map_config(self):
        x = self.x_map_size_spinbox.value()
        y = self.y_map_size_spinbox.value()
        self.canvas.scene.initialize_scene(self.map_config_combobox.currentText(),size=(x,y))

    def set_fps_logging(self):
        if self.log_fps_checkbox.isChecked():
            self.canvas.fps_log_timer.start(2000)
        else:
            self.canvas.fps_log_timer.stop()
    
    def set_fps_display(self):
        if self.display_fps_checkbox.isChecked():
            self.canvas.camera.display_fps_overlay = True
        else:
            self.canvas.camera.display_fps_overlay = False
