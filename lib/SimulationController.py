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

    def __init__(self,canvas):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.canvas = canvas
        self.is_shutting_down = False

        uic.loadUi(f'{self.file_paths.user_path}ui/simulation_controller.ui',self)
        self.setWindowTitle('Simulation Controller')
        self.create_button.clicked.connect(self.apply_settings)

        self.apply_settings()

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Escape:
            self.logger.log(f'Sending shutdown signal...')
            self.shutdown_signal.emit()
        elif key == Qt.Key_1:
            self.close()

    def closeEvent(self, e):
        if not self.is_shutting_down:
            self.logger.log('Shutdown signal received.')
            self.is_shutting_down = True
        self.shutdown()
    
    def shutdown(self):
        self.close()

    def apply_settings(self):
        self.set_map_config()
        self.update_map_configs_combobox()
        self.set_fps_logging()
        self.set_fps_display()

    def update_map_configs_combobox(self):
        self.map_config_combobox.addItems(self.canvas.scene.map.map_configs)

    def set_map_config(self):
        idx = self.map_config_combobox.currentIndex()
        self.logger.log(f'Setting map index: {idx}')

        x = self.x_map_size_spinbox.value()
        y = self.y_map_size_spinbox.value()
        self.canvas.scene.initialize_scene(size=(x,y))

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
        
