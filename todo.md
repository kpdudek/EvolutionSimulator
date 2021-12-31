Simulation controller
- Add an option to save the current config as default
- Separate UI into simulation creator, display settings (can be updated during a simulation), ...

Generate rabbits
- size and color determine attractiveness
- eat grass and drink water

Generate foxes
- eat rabbits
- fight with eachother for control of land

Generate terrain
- 2D perlin noise generates a tile map
- each tile has a terrain type, moisture content (with water being unique at 100), color, etc.
- generate food
- Add saving capability
- Merge similar tiles into one polygon to reduce number of draw calls
- Stop generating Noise for every map config. Only do it for the selected map.
- Generate a graph over movable tiles, so entites can use it for planning
    - Implement A* search

Game Rules:
- Moving costs energy (in units of calories)
- Eating another entity is a net gain of that entitiy's (energy_density * mass * health)

Camera
- Add acceleration on movements

Questions:
- Figure out pixmap shading so lighting is possible and dynamic color changing (eg. for coat color)
- How many tiles can I draw at once? This will be a chunk.
- Should I paint directly on a QLabel or should I use QGraphicsScene