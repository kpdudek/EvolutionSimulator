#!/usr/bin/env python3

from PyQt5.QtWidgets import QMainWindow, QCheckBox, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic

from lib.Logger import FilePaths, Logger

class KeyControls(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()

        uic.loadUi(f'{self.file_paths.user_path}ui/keycontrols.ui',self)
        self.setWindowTitle('Key Controls')

        self.qt_key_map = {}
        self.key_map ={}
        self.generate_key_dict()
        self.populate_key_lists()

    def generate_key_dict(self):
        self.qt_key_map = {
                            "W":Qt.Key_W,
                            "S":Qt.Key_S,
                            "A":Qt.Key_A,
                            "D":Qt.Key_D,
                            "C":Qt.Key_C,
                            "1":Qt.Key_1
                            }

        self.key_map = {
                        "Camera Forward":"W",
                        "Camera Backward":"S",
                        "Camera Left":"A",
                        "Camera Right":"D",
                        "Center Camera":"C",
                        "Open Simulation Controller":"1",
                        }
    
    def populate_key_lists(self):
        for key,assignment in list(self.key_map.items()):
            self.key_list.addItem(key)
            self.assignment_list.addItem(assignment)


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

        self.key_controls = KeyControls()
        self.controls_button.clicked.connect(self.key_controls.show)

        self.create_button.clicked.connect(self.apply_settings)
        self.action_save_default.triggered.connect(self.save_as_default)
        self.action_load_default.triggered.connect(self.load_default)

        for widget in self.display_settings_frame.children():
            if isinstance(widget,QCheckBox):
                widget.toggled.connect(self.update_display_settings)

        self.apply_settings()
        self.update_display_settings()
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
        self.setGeometry(0,30,self.size().width(),self.size().height())
        self.setFocus()

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
        self.map_config_combobox.addItems(self.canvas.scene.map.map_config_names)

    def validate_spinboxes(self):
        '''
            This function ensures that the chunk size is a multiple of 2 so that the fractal noise octave
            is valid.
        '''
        x = self.x_map_size_spinbox.value()
        if x%2 != 0:
            x+=1
            self.x_map_size_spinbox.setValue(x)
        y = self.y_map_size_spinbox.value()
        if y%2 != 0:
            y+=1
            self.y_map_size_spinbox.setValue(y)

    def apply_settings(self):
        '''
            Generate a new simulation by calling each settings method
        '''
        self.validate_spinboxes()
        self.set_map_config()
        self.update_display_settings()
        self.canvas.camera.reset()
    
    def update_display_settings(self):
        self.set_fps_logging()
        self.set_fps_display()
        self.set_border_display()
        self.set_path_display()
        self.set_debug_mode()

    ####################################################################################################
    #   Settings Methods:
    #       The following methods implement the actions needed to generate a new simulation.
    #       The apply_settings() method calls each of these methods to generate a new simulation.
    ####################################################################################################
    def set_map_config(self):
        x = self.x_map_size_spinbox.value()
        y = self.y_map_size_spinbox.value()
        config_name = self.map_config_combobox.currentText()
        tile_size = self.tile_size_spinbox.value()
        food_count = self.food_count_spinbox.value()
        prey_count = self.prey_count_spinbox.value()
        predator_count = self.predator_count_spinbox.value()
        num_entities = food_count + prey_count + predator_count
        num_tiles = x * y
        if num_entities > num_tiles:
            self.logger.log(f"A simualtion was generated with {num_entities} entities but only {num_tiles} tiles!",color='r')
            return
        
        # Clear the Scene and generate a new one based on the parameters         
        self.canvas.scene.initialize_scene(
                                            config_name,
                                            tile_size=tile_size,
                                            size=(x,y),
                                            food_count=food_count,
                                            prey_count=prey_count,
                                            predator_count=predator_count)

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

    def set_border_display(self):
        if self.display_borders_checkbox.isChecked():
            self.canvas.borders_visible(True)
        else:
            self.canvas.borders_visible(False)

    def set_path_display(self):
        if self.display_paths_checkbox.isChecked():
            self.canvas.camera.draw_paths = True
        else:
            self.canvas.camera.draw_paths = False

    def set_debug_mode(self):
        if self.debug_mode_checkbox.isChecked():
            self.canvas.scene.debug_mode = True
            self.canvas.camera.debug_mode = True
        else:
            self.canvas.scene.debug_mode = False
            self.canvas.camera.debug_mode = False
