#!/usr/bin/env python3

from PyQt5 import QtCore

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import lib.Errors as errors
from lib.Map import Map

import numpy as np

class Camera(object):
    def __init__(self,window_size,painter,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.window_size = window_size
        self.painter = painter
        self.scene = scene
        self.zoom_level = 1.0
        self.draw_borders = False
        self.draw_paths = False

        self.frames = {
            'camera':np.array([0.0,0.0]),
            'scene':np.array([0.0,0.0])
            }

        self.display_fps_overlay = True

    def reset(self):
        if isinstance(self.scene.map,Map):
            pix_size = self.scene.map.pix_size
            offset = (pix_size - self.window_size.copy())/2
            self.teleport(offset)

    def teleport(self,pose):
        self.frames['scene'] = pose
    
    def translate(self,vec):
        self.frames['scene'] = self.frames['scene'].copy() + -1*vec

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

    def clear_display(self):
        self.paint_utils.set_color(self.painter,'light_gray',True)
        self.painter.drawRect(0,0,self.window_size[0],self.window_size[1])

    def fps_overlay(self,fps):
        if self.display_fps_overlay:
            self.paint_utils.set_color(self.painter,'black',True)
            self.painter.drawText(3,13,200,75,QtCore.Qt.TextWordWrap,str(int(fps)))

    def paint_entity(self,entity):
        if entity.config['type'] == 'map':
            prev_color = None
            for row in entity.tiles:
                for tile in row:
                    if tile.color.toRgb() != prev_color:
                        self.painter.setPen(tile.pen)
                        self.painter.setBrush(tile.brush)
                        prev_color = tile.color.toRgb()
                    pose = self.transform(tile.pose.copy())
                    self.painter.drawRect(pose[0],pose[1],tile.size[0],tile.size[1])
        elif entity.config['type'] in ['prey','predator','food']:
            pose = self.transform(entity.config['pose'].copy())
            self.painter.drawPixmap(pose[0],pose[1],entity.pixmap)
            if self.draw_borders:
                self.painter.setPen(entity.pen)
                self.painter.setBrush(entity.brush)
                self.painter.drawRect(pose[0],pose[1],entity.bounding_size[0],entity.bounding_size[1])
            if isinstance(entity.path,np.ndarray) and self.draw_paths:
                if entity.config['type'] == 'prey':
                    self.paint_utils.set_color(self.painter,'black',True,width=3)
                elif entity.config['type'] == 'predator':
                    self.paint_utils.set_color(self.painter,'red',True,width=3)
                r,c = entity.path.shape
                for idx in range(0,c-1):
                    pose1 = self.transform(entity.path[:,idx])
                    pose2 = self.transform(entity.path[:,idx+1])
                    self.painter.drawLine(pose1[0],pose1[1],pose2[0],pose2[1])

                self.paint_utils.set_color(self.painter,'start_pose',True)
                s = self.transform(entity.path[:,0])
                self.painter.drawEllipse(s[0],s[1],8,8)

                self.paint_utils.set_color(self.painter,'goal_pose',True)
                g = self.transform(entity.path[:,-1])
                self.painter.drawEllipse(g[0],g[1],8,8)
        
    def update(self):
        '''
            Draws all entities in the scene.
        '''
        self.paint_entity(self.scene.map)
        for entity_type in self.scene.entities.values():
            for entity in entity_type.values():
                self.paint_entity(entity)
