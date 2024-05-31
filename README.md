# Pycosystem

## Introduction

Pycosystem is a basic ecosystem simulation using Pygame. While not nearly as advanced or realistic as a full ecosystem, this program aims to examine the basics of genome inheritance and behavior. It is run from it’s corresponding file (pycosys.py) and requires no additional parameters.

The simulation consists of three different types of animals: omnivores (represented through brown ”bears”), carnivores (represented by foxes) and herbivores (represented by bunnies).

When the simulation is started it will create an instance of the world-class, which handles all animal instances as well as drawing and updating all sprites.

The world consists of 3 parts: water tiles, grass tiles and berry bushes. When an instance of the world-class is created, it will generate the map. This is done by generating a random map using Perlin-Noise.

While the world is ”running”, it will update all alive animal sprites and then iterate through all alive animals and trigger their alive-function and, depending on the return value, act accordingly.

## World generation

The world generation is done using Perlin-Noise. Due to the generated noise being only pseudo-random, it is commonly used for scenarios as this, because it generates coherent textures, similar to actual landmasses. Also, since the implementation is seeded, the same seed will always generate the same landmass, which makes testing with different animal-ratios or placements much easier. The algorithm uses four octaves, meaning the following process is run four times with an increasing frequency, generating a very smooth looking image.

At first, 50 evenly spaced numbers in the interval $(0,f)$, where $f=2^i$ with $i$ being the current octave, are created. These are then mapped along the x- and y-axis, creating a meshgrid. After that, the program creates the permutation array with the numbers $[0,255]$ randomly placed in it. This array is then joined along the y-axis with itself, creating a 2D-array, and after that reduced back into a 1D-array for easier dot product interpolation. We then take the grid coordinates of the meshgrid created earlier to calculate the distance vector coordinates.

Using the distance vectors, the gradient vectors for each corner of a cell are calculated. To further smoothen the result, the coordinates of the distance vectors (x and y respectively) are then run through the smoothstep function of 5th order $(6x^5-15x^4+10x^3)$ to create a fade. As a last step, using linear interpolation, the fades are then applied to the gra- dient vectors. This results in a grid filled with values that seem random, but which are actually dependent/based on each other.

This process is repeated for all four octaves, with the results added onto themselves to create a noise-map.

The array containing the calculated values is then converted into a tilemap using certain thresholds. If a cell has a very high - or low - value it becomes a water tile, otherwise it will become a land tile. All landtiles are also copied into a second array to make placing berries and animals easier.

The process is rather simple, we calculate the total ”landmass” (the size of the array) and then multiply it by a predefined percentage (found in the settings file) of land which should be covered with either berries, herbivores, omnivores or carnivores.

The algorithm randomly selects a landtile from the landmass-array, places the according thing(berry, herbi,...) on top of it and removes the tile from the array to ensure that no overwrites can occur. This is done until all percentages are satisfied. The finished map is then returned to the world-class, where it is converted into images on the screen.

## Simulating the animals

### General setup

At first, it is important to discuss how the animals act and what is needed for that. While an animal is alive it will walk around randomly, this is called *normal movement*. While in this state, a direction is chosen randomly and the animal will walk to the next tile in that direction, if possible.

If it reaches a predefined threshold of either hunger or thirst, it will pathfind to the nearest food or water source.

If it is neither hungry northirsty and is already mature, it will try to find a mate. If the mating process was successful a cooldown will trigger, during which no mating can occur.

While eating, drinking or mating the animal becomes ”frozen” for 10 ticks, meaning nothing else will occur. This is to represent more realistic behavior, since all of these processes take time.

To ensure no animal is trying to mate with itself or another invalid target, they get passed a dictionary containing all alive animals of the same type as well as a key which corresponds to their entry in the dictionary.

If the animal’s hunger or thirst threshold reaches 1000, or it’s maximum age got reached, the animal will die.

It is important to note that all individual values (max age, hunger- and thirst-rate) are inherited through genomes. Although only the dominant value will be represented in the world, both alleles will be used during the mating/inheritance process. This means that both the dominant and recessive values get stored in the dictionary. At startup, every animal will receive a set of randomly generated genomes.

### Type Setups and Differences

#### Carnivores

Carnivores are the closest type of animal to their parent class. They follow the basic alive-routine, but need to hunt herbivores for food. In order for that to work, they get passed another dictionary containing all alive animals which are huntable. If the carnivore needs to find food, it will check in a square around itself, which increases in size if nothing is found, for a valid target. If one is found, it will become hunted and the carnivore will pathfind to it.

#### Herbivores

Herbivores deviate a bit more from their parent class, as they can become hunted and need to pass on some additional information. They feed off berries, which they find in a similar fashion as the carnivores, but instead of searching through a dictionary containing all the berries, they just search through the map-array to find a cell with a berry value. While a herbivore is hunted, it will pass on it’s movement to it’s hunter, in order for the hunter to actually find it’s prey.

#### Omnivores

Omnivores are essentially a combination of both carnivores and herbivores. They will eat berries if not too hungry, but will also resort to hunting other animals if necessary.

### Path finding

The path finding is done using a standard A*-algorithm. While I will not go into detail as to how A* works (since there are plenty of explanations on the web), it is worth noting that the algorithm is run multiple times during hunting. This is to shorten the path a hunter needs to get to its prey, since the movements of the prey just get appended to the movements of the hunter. It also makes for a more "realistic" hunting behavior, since hunting animals usually don't mindlessly run after their prey.

### Inheritance

The process of finding a mate works identical to finding prey, just with the aforementioned conditions.

If the two animals have reached the same tile, the actual mating process occurs. During this, the genomes of the parents get passed into a function which then generates the inherited values of the child.

For every genome (that being maximum age, thirst- and hunger-rate), the function first randomly (with a chance of $\frac{1}{2}$) selects either the mothers or fathers dominant gene of the corresponding type. After that it will randomly assign it to either stay dominant or become recessive, with a $\frac{3}{4}$ chance to stay dominant. The other value gets assigned to the other allele. (i.e. if male dominant gets chosen and becomes recessive, the female recessive becomes the new dominant)

At the end, there is a $\frac{1}{20}$ chance for the genes to mutate. In the case that mutation occurs, for every gene, a random value, out of the interval which both the dominant and recessive values create, is chosen and divided by 4. After that it will either get subtracted or added onto both alleles, with the chances being equally distributed.

Let $i\in Genomes$, then this process could be described as $\forall i: i = i \pm \frac{[i_{dom},i_{rec}]}{4}$.

## The problem with Multiprocessing

### Implementation in one simulation

To improve the simulation performance I planned on implementing some form of multipro- cessing. My first thought was to split the pathfinding algorithm into multiple processes. While easy in theory, the actual implementation wasn’t really working. Due to how the A*-algorithm is ”looking ahead” to pick the most promising move, the processes would all pick the same cell, rendering them useless. Also, to prevent overrides from happening in the hash-map, every single process would need it’s own hash-map, making the algorithm even more memory-hungry than it already is. So this idea was quickly scrapped and I continued to ponder over how to improve performance.

The next logical step was to move ”further outside” of the simulation. I thought about splitting the animals into several processes, so the simulation could handle multiple alive- routines at once, hence boosting the performance by how many processes were running at once. But I also quickly ran into problems here.

Due to how the animals interact with one another, there are several scenarios where they become dependent one each other; i.e. while hunting/being hunted and during mating. So there is a high likelihood that a deadlock between two animals occurs. Without fun- damentally changing the way the animals behave and interact, or by including a lot of locks (which I wasn’t sure would solve the problem in all cases), there was no real way to safely implement this.

### Running multiple simulations

Since my attempts to parallelize processes in one simulation were rather futile, I thought again to myself: ”Move further outside.” So I did just that.

I had the idea to run several instances of the simulation simultaneously, with the same map, and to analyze certain parameters (gene distribution etc.) in real time. For this I wrote an analyzer-module, which created several matplotlib-subplots to visualize the data and update them. With this done, I just had to run multiple instances of the world- class and extract the necessary data. But here was where I encountered yet another error, which ultimately led me to the conclusion that implementing multiprocessing wasn’t really feasible. Due to the nature of the error I want to explain it in further detail.

Processes do not share memory space, meaning they need some other way to communicate and send data between each other; this is done through serialization. I found a great explanation by Matthew Rockling on how serialization works:

*Think of a teleporter in Star Trek: An item or crew member (data) is translated into something small and manageable (text or bits), which is then quickly moved to some other location and (hopefully) reassembled correctly.*

The serialization and translation of data between processes using the multiprocessing- library is handled by the serialization package pickle. While the package can handle most objects and functions, it struggles with a few things, including: lambdas, closures, methods.

Because all animal types inherit their methods from the animal-class, this was a huge problem. Basically I’d need to restructure all classes and their methods, or write a wrapper-function as a workaround. Because pickle is apparently fine when it needs to serialize a function which then makes a method-call of some class. After writing a wrapper and adjusting a few more things I encountered the final problem.

For convenience (mainly) all animals are Pygame-sprites. This makes drawing them to the screen really easy and also provides advantages in moving them around and letting them interact with another. The problem is that all of these sprites are considered surfaces, which are not serializable. In fact, most Pygame-objects aren’t serializable at all due to how they’re coded. I don’t really understand why I didn’t encounter this problem earlier, but at this point I can only guess.

While there is an alternative library to pickle called dill, it seems that it also isn’t really able to serialize Pygame-objects.

At this point, multiprocessing isn't really implementable due to how the code is structured. I might come back to this project and restructure the classes, but that's a big maybe.
