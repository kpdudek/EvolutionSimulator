#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import QPointF

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import lib.Geometry as geom
import lib.Errors as errors
import numpy as np

class Camera(object):
    def __init__(self,frame_size,painter,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.frame_size = frame_size
        self.painter = painter
        self.scene = scene
        self.zoom_level = 1.0

        self.frames = {
            'camera':np.array([0.0,0.0]),
            'scene':np.array([0.0,0.0])
            }

        self.display_fps_overlay = True
        self.display_tails = False

    def reset(self):
        self.teleport(np.zeros((2)))

    def teleport(self,pose):
        self.frames['scene'] = pose
    
    def translate(self,vec):
        self.frames['scene'] = self.frames['scene'] + -1*vec

    def zoom(self,multiplier):
        self.zoom_level = multiplier

    def transform(self,point,parent_frame='camera',child_frame='scene'):
        '''
        Transforms a point from the parent frame to the child frame.
        Default behavior is camera frame -> scene frame.
        '''
        if child_frame not in list(self.frames.keys()):
            raise errors.FrameNotFound(child_frame)
        if parent_frame not in list(self.frames.keys()):
            raise errors.FrameNotFound(child_frame)
        
        coord = point + (self.frames[parent_frame] - self.frames[child_frame])
        return coord

    def clear_display(self,fps):
        self.paint_utils.set_color(self.painter,'light_gray',True)
        self.painter.drawRect(0,0,self.frame_size[0],self.frame_size[1])

        if self.display_fps_overlay:
            self.paint_utils.set_color(self.painter,'black',True)
            self.painter.drawText(3,13,200,75,QtCore.Qt.TextWordWrap,str(int(fps)))

    def paint_entity(self,entity):
        if entity.config['type'] == 'map':
            prev_color = None
            for tile in entity.tiles:
                if tile.color.toRgb() != prev_color:
                    self.paint_utils.set_color(self.painter,tile.color,True)
                    prev_color = tile.color.toRgb()
                self.painter.drawRect(tile.pose[0],tile.pose[1],tile.size[0],tile.size[1])
        
    def update(self):
        '''
            Draws all entities in the scene.
        '''
        for entity in self.scene.entities.values():
            self.paint_entity(entity)

        self.paint_utils.set_color(self.painter,'black',True)
        self.painter.drawRect(200,200,22,22)