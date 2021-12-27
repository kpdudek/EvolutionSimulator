#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from lib.Canvas import Canvas
from lib.Logger import Logger

import sys

def main():
    logger = Logger()
    logger.insert_blank_lines(2)
    
    logger.log("Simulation starting...")
    app = QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    canvas = Canvas(screen_resolution)
    app.exec_()
    logger.log("Simulation ended.")

if __name__ == '__main__':
    main()