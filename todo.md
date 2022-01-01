Simulation controller
- Allows a simulation to be run based on a set of entity properties and simulation rules.
- Add an option to save the current config as default.

Game Objects
- Simulate the life cycle of a plant or animal.
- Created with a set of traits, and their descendents can inherit those traits.
- Upon creation, there is a chance of mutation.
- Moving costs energy (in units of calories).
- When energy reaches zero, the entity dies.
- Eating another entity is a net gain of that entitiy's (energy_density * mass * health).
- Entities strive to reproduce.
    - End of life for a plant distributes it's seeds.
    - Animals reproduce based on a set of attractiveness traits.

Generate Predators
- Carnivores
- Eat Prey game objects, but not Food objects
- fight with eachother for control of land

Generate Prey
- Herbivores
- Eat Food game objects, and eaten by Predator objects

Generate food 
- Plants
- Eaten by Prey, and consumes natural resources (sunlight, water, CO2)

Generate Terrain
- 2D perlin noise generates a tile map
- Each tile has a terrain type, moisture content (with water being unique at 100), color, etc.
- Terrain is saveable.
- Merge similar tiles into one polygon to reduce number of draw calls.
- Generate a graph over movable tiles, so entites can use it for planning
    - Implement A* search

Scene
- Stores the world position of all entities

Camera
- Allows panning and zooming.
- Add acceleration on movements.
- Render entities in order food, prey, predator

Questions:
- Figure out pixmap shading so lighting is possible and dynamic color changing (eg. for coat color).
- How many tiles can be drawn at once? What if similar neighbors are used to reduce draw calls?
