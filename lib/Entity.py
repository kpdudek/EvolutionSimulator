#!/usr/bin/env python3

from PyQt5.QtWidgets import QWidget

class Entity(QWidget):
    def __init__(self,fps,game_manager):
        super().__init__()