#!/usr/bin/env python3

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtGui
from numpy.lib.shape_base import _tile_dispatcher

from lib.Camera import Camera
from lib.Logger import Logger
from lib.Scene import Scene

import numpy as np
import time, math

class Canvas(QLabel):
    '''
    This class initializes the window
    '''
    shutdown_signal = pyqtSignal()
    def __init__(self,screen_resolution):
        super().__init__()
        window_size = [800,800]
        self.screen_width, self.screen_height = screen_resolution.width(), screen_resolution.height()
        offset_x = int((self.screen_width-window_size[0])/2)
        offset_y = int((self.screen_height-window_size[1])/2)
        self.setGeometry(offset_x,offset_y,window_size[0],window_size[1])
        self.setWindowTitle('PyEvolution')

        self.simulation_controller = None
        self.is_shutting_down = False
        self.keys_pressed = []
        self.debug_mode = False
        self.fps = 50.0
        self.loop_fps = -1.0
        self.painter = None
        
        self.camera = None
        self.resize_canvas(window_size[0],window_size[1])
        self.logger = Logger()
        self.scene = Scene(self.fps)
        self.camera = Camera(np.array([900,900]),self.painter,self.scene)

        self.game_timer = QTimer()
        self.game_timer.timeout.connect(self.game_loop)
        self.game_timer.start(1000/self.fps)

        self.fps_log_timer = QTimer()
        self.fps_log_timer.timeout.connect(self.fps_log)

        self.setFocusPolicy(Qt.StrongFocus)
        self.show()

    def borders_visible(self,bool):
        if bool:
            self.scene.map.tile_borders_visible(True)
            self.camera.draw_borders = True
        else:
            self.scene.map.tile_borders_visible(False)
            self.camera.draw_borders = False

    def resize_canvas(self,width,height):
        if isinstance(self.painter,QtGui.QPainter):
            if self.painter.isActive():
                self.painter.end()

        self.frame_size = np.array([width,height])
        self.canvas_pixmap = QtGui.QPixmap(self.frame_size[0],self.frame_size[1])
        self.setPixmap(self.canvas_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())

        if isinstance(self.camera,Camera):
            self.camera.painter = self.painter
            self.camera.frame_size = self.frame_size

    def resizeEvent(self, e):
        self.resize_canvas(e.size().width(),e.size().height())

    def closeEvent(self, e):
        if not self.is_shutting_down:
            self.logger.log('Shutdown signal received.')
            self.is_shutting_down = True
        self.shutdown_signal.emit()
        self.shutdown()

    def shutdown(self):
        if self.painter.isActive():
            self.painter.end()
        self.close()

    def mousePressEvent(self, e):
        button = e.button()
        pose = np.array([e.x(),e.y()])
        self.logger.log(f'Mouse press ({button}) at: [{pose[0]},{pose[1]}]')

        # Must convert the camera frame point to the scene and find which tile the mouse collides with
        pose_t = self.camera.transform(pose,parent_frame='scene',child_frame='camera')
        tile_press,idx = self.scene.map.tile_at(pose_t)
        self.logger.log(f'Tile selected: [{tile_press[0]},{tile_press[1]}]')
        self.logger.log(f'Tile index: {idx}')
    
    def keyPressEvent(self, event):
        key = event.key()              
        if key == Qt.Key_Escape:
            self.shutdown()
        elif key == Qt.Key_1:
            if self.simulation_controller.isVisible():
                self.simulation_controller.hide()
            else:
                self.simulation_controller.show()
        else:
            if key not in self.keys_pressed:
                self.keys_pressed.append(key)

    def keyReleaseEvent(self, event):
        if not event.isAutoRepeat() and event.key() in self.keys_pressed:
            self.keys_pressed.remove(event.key())

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

    def fps_log(self):
        self.logger.log(f'Max FPS: {self.loop_fps}')
        if self.loop_fps<self.fps:
            self.logger.log("FPS has dropped below the set value.",color='y')

    def game_loop(self):
        tic = time.time()
        self.process_keys()
        self.camera.clear_display()
        self.camera.update()
        self.camera.fps_overlay(self.loop_fps)
        self.repaint()
        toc = time.time()

        # Calculate max FPS
        loop_split = toc-tic
        if loop_split > 0.0:
            self.loop_fps = 1.0/(toc-tic)
