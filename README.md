# Pycosystem
Pycosystem is a basic ecosystem simulation using PyGame. While not nearly as advanced or realistic as a full ecosystem, this program aims to examine the basics of genom inheritance and behavior.
The simulation consists of three different types of animals: omnivores (represented in gray), carnivores (represented in black) and herbivores (represented in white). The program is run from it's corresponding file, which just consists of a basic PyGame run-loop.
When the simulation is started it will create an instance of the world class, which handles all animal instances as well as drawing and updating all sprites.
The world consists of 3 parts: water tiles (blue), grass tiles (green) and berry tiles (red). When an instance of the World class is created, it will generate the map. This is done by reading the contents of a CSV-file, which was generated using a program called \textit{Tiled}. Every cell of the CSV contains a floating point number representing a certain sprite. The function just iterates through the entire CSV and, depending of the float, draws the sprite on it's corresponding location on the screen.
While the world is "run", it will update all alive animal sprites and then iterate through all alive animals and trigger their alive-function and, depending on the return value, act accordingly.