# Pycosystem

## Introduction and world simulation

Pycosystem is a basic ecosystem simulation using PyGame. First and foremost, I wrote this programm as an exercise for myself, but also as an exam assignment for a class I am taking at university.

While not nearly as advanced or realistic as a full ecosystem, this program aims to examine the basics of genom inheritance and behavior.

The simulation consists of three different types of animals: omnivores (represented in gray), carnivores (represented in black) and herbivores (represented in white). The program is run from it's corresponding file, which just consists of a basic PyGame run-loop.

When the simulation is started it will create an instance of the world class, which handles all animal instances as well as drawing and updating all sprites.

The world consists of 3 parts: water tiles (blue), grass tiles (green) and berry tiles (red). When an instance of the World class is created, it will generate the map. This is done by reading the contents of a CSV-file, which was generated using a program called *Tiled*. Every cell of the CSV contains a floating point number representing a certain sprite. The function just iterates through the entire CSV and, depending of the float, draws the sprite on it's corresponding location on the screen.

While the world is "run", it will update all alive animal sprites and then iterate through all *alive* animals and trigger their *alive*-function and, depending on the return value, act accordingly.

## Simulating the animals

### General setup

At first, it is important to discuss how the animals act and what is needed for that. While an animal is alive it will first walk around randomly, this is called the normal movement. While in this state, a direction is chosen randomly and the animal will walk to the next tile in that direction if possible.

When it reaches a predefined threshold of either hunger or thirst, it will path find (discussed later) to the nearest food or water source. If it is neither hungry nor thirsty and is already mature, it will try to find a mate. If the mating process was successful a cooldown will trigger, during which no mating can occur. To ensure no animal is trying to mate with itself or another invalid target, they get passed a dictionary containing all alive animals of the same type, as well as a key which corresponds to their entry in the dictionary.

If the animals hunger or thirst threshold reaches 100, or if it's age reaches 100, the animal will die.

It is important to note that all individual values (max age, hunger- and thirst-rate) are inherited through genomes. Although only the dominant value will be represented in the world, both alleles will be used during the mating/inheritance process. At startup, every animal will receive a set of randomly generated genomes.

### Type Setups and Differences

#### Carnivores

Carnivores are the closest type of animal to their parent class. They follow the basic *alive*-routine, but need to hunt **Herbivores** for food. In order for that to work, they get passed another dictionary containing all alive animals which are huntable. If the carnivore needs to find food, it will check in a square around itself, which increases in size if nothing is found, for a valid target. If one is found, it will become hunted and the carnivore will path find to it.

#### Herbivores

Herbivores deviate a bit more from their parent class, as they can become hunted and need to pass on some additional information. They feed off berries, which they find in a similar fashion as the **Carnivores**, but instead of searching through a dictionary containing all the berries, they just search through the map CSV to find a cell with the berry value.

While a herbivore is hunted, it will pass on it's movement to it's hunter, in order for the hunter to actually find it's prey.

#### Omnivores

Omnivores are essentially a combination of both **Carnivores** and **Herbivores**. They prefer to hunt, but if they can't find prey or if their hunger is to high, they will also resort to eating berries.

### Path finding

The path finding is done using a standard A*-algorithm. While I will not go into detail as to how A* works (since there are plenty of explanations on the web), it is worth noting that the algorithm is run multiple times during hunting. This is to shorten the path a hunter needs to get to its prey, since the movements of the prey just get appended to the movements of the hunter. It also makes for a more "realistic" hunting behavior, since hunting animals usually don't mindlessly run after their prey.

### Inheritance

The process of finding a mate works identical to finding prey, just with the aforementioned conditions.

If the two animals have reached the same tile, the actual mating process occurs. During this, the genomes of the parents get passed into a function which then generates the inherited values of the child.

For every genome (that being maximum age, thirst- and hunger-rate), the function first randomly (with a chance of 1/2) selects either the mothers or fathers dominant gene of the corresponding type. After that it will randomly assign it to either stay dominant or become recessive, with a 3/4 chance to stay dominant.

At the end, there is a 1/20 chance for the genes to mutate. During this, for every gene, a random value, out of the interval which both the dominant and recessive values create, is chosen and divided by 4. After that it will either get subtracted or added onto both alleles, with the chance being equally distributed.

## Closing thoughts

There is still a lot of room for improvement. First and foremost there would be the obvious graphics. While they certainly do their job, they are more or less just functionally oriented.

There is also the possibility for a randomized map. At this stage, the map and animal placement is always identical and to create a new map would mean to create an entire new world in *Tiled*. While the random movement and inheritance process already ensure that no simulation will be the same, it would be a great improvement.

At last, there is also room for a more sophisticated inheritance system. Currently only 3 properties become inherited, but in reality there are a lot more things, like speed, size etc. It is also not unreasonable to think about an improved mutation system.

But despite all this, I think Pycosystem is in a great stage.
