#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui

from lib.SimulationController import SimulationController
from lib.Camera import Camera
from lib.Logger import Logger
from lib.Scene import Scene

import numpy as np
import time

class Canvas(QLabel):
    '''
    This class initializes the window
    '''
    def __init__(self,screen_resolution):
        super().__init__()
        window_size = [800,800]
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((self.screen_width-window_size[0])/2)
        offset_y = int((self.screen_height-window_size[1])/2)
        self.setGeometry(offset_x,offset_y,window_size[0],window_size[1])
        self.setWindowTitle('PyEvolution')

        self.keys_pressed = []
        self.debug_mode = False
        self.fps = 30.0
        self.loop_fps = -1.0
        self.painter = None

        self.resize_canvas(window_size[0],window_size[1])
        self.logger = Logger()
        self.scene = Scene(self.fps)
        self.camera = Camera(np.array([900,900]),self.painter,self.scene)
        # self.simulation_controller = SimulationController(self.scene,self.camera)

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000/self.fps)

        self.fps_log_timer = QTimer()
        self.fps_log_timer.timeout.connect(self.fps_log)
        self.fps_log_timer.start(2000)

        self.show()

    def resize_canvas(self,width,height):
        try:
            self.painter.end()
        except:
            pass
        self.frame_size = np.array([width,height])
        self.canvas_pixmap = QtGui.QPixmap(self.frame_size[0],self.frame_size[1])
        self.setPixmap(self.canvas_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())
        try:
            self.camera.painter = self.painter
            self.camera.frame_size = self.frame_size
        except:
            pass
        self.resize_flag = False

    def resizeEvent(self, e):
        self.resize_canvas(e.size().width(),e.size().height())

    def keyPressEvent(self, event):                
        if event.key() == Qt.Key_Escape:
            self.shutdown()
        else:
            if event.key() not in self.keys_pressed:
                self.keys_pressed.append(event.key())

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

    def closeEvent(self, e):
        self.logger.log('Shutdown signal received.')
        self.shutdown()

    def shutdown(self):
        self.close()
        # if self.simulation_controller.isEnabled():
        #     self.simulation_controller.close()

    def fps_log(self):
        self.logger.log(f'Max FPS: {self.loop_fps}')

    def process_keys(self):
        cam_speed = 3.0
        for key in self.keys_pressed:
            if key == Qt.Key_A:
                self.camera.translate(np.array([cam_speed,0.0]))
            elif key == Qt.Key_D:
                self.camera.translate(np.array([-cam_speed,0.0]))
            elif key == Qt.Key_W:
                self.camera.translate(np.array([0.0,cam_speed]))
            elif key == Qt.Key_S:
                self.camera.translate(np.array([0.0,-cam_speed]))
            elif key == Qt.Key_R:
                self.camera.reset()

    def game_loop(self):
        tic = time.time()
        self.process_keys()
        self.camera.clear_display()
        self.camera.update()
        self.camera.fps_overlay(self.loop_fps)
        self.repaint()
        toc = time.time()

        try:
            self.loop_fps = 1.0/(toc-tic)
        except:
            pass
