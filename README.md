# EvolutionSimulator
Simulating a predator prey relationship in a 2D world using PyQt5.

## Installation
To run the game you will need to install:
* python3
* pip3
* numpy
* PyQt5
* git (reccomended)

#### *Ubuntu 18.04:*
```
sudo apt install git python3 python3-pip
git clone https://github.com/kpdudek/EvolutionSimulator.git
pip3 install PyQt5 numpy
```

#### *Windows 10:*
Download python >3.7 from the Microsoft Store and then use pip3 (included in the Microsoft Store download) to install PyQt5 and numpy.

Install git as described [here](https://www.computerhope.com/issues/ch001927.htm#:~:text=How%20to%20install%20and%20use%20Git%20on%20Windows,or%20fetching%20updates%20from%20the%20remote%20repository.%20)
```
git clone https://github.com/kpdudek/EvolutionSimulator.git
pip3 install PyQt5 numpy
```

## Game Play
After installation, launch the game by navigating to the `EvolutionSimulator` repo you just cloned (or downloaded) and then executing the `main.py` file as follows:
```
/path/to/EvolutionSimulator> python3 main.py 
```

A window will open with a randomly generated map. To adjust the simulation settings, press `1` to show the simulation controller.
## Controls
Camera Pan : WSAD

Reset Camera : R

Open Simulation Controller : 1