from World.tile import Tile
from settings import *
import pygame as pg
import random as rnd
import numpy as np
import astar as ast


class Animal(Tile):
    def __init__(
        self,
        pos: tuple,
        genomes: dict,
        population: dict,
        map: list,
        key: int,
        sprite: str,
        group,
    ) -> None:
        """Initalizing function.

        Args:
            pos (tuple): position the animal gets spawned at
            genomes (dict): the genome values of the animal
            population (dict): all alive animals of the same type
            map (list):
            key (int): key which correspones to the dictionary entry of the animal
            sprite (str):
            group (_type_):
        """
        super().__init__(pos, sprite, group)

        self.pos = pos
        self.genomes = genomes
        self.map = map
        self.population = population
        self.key = key

        self.age = 0
        self.type = self.genomes["animal_type"]
        self.max_age = self.genomes["max_age_d"]
        self.hunger = 0
        self.hunger_rate = self.genomes["hunger_rate_d"]
        self.thirst = 0
        self.thirst_rate = self.genomes["thirst_rate_d"]

        # movement related variables
        self.queued_movements = []
        self.path_length = None

        # nutrient related variables
        self.food_found = False
        self.water_found = False
        self.food_point = None
        self.water_point = None

        # mating related variables
        self.mate = None  # gets set to the corresponding animal
        self.mate_pos = None  # only gets set for the searching animal
        self.cooldown = None  # mating cooldown

    def __cleanup_on_death__(self) -> None:
        """Cleanup function if the animal dies."""
        if self.mate:
            self.mate.mate = None
            self.mate.mate_pos = None
            self.mate.queued_movements = []

    def alive(self) -> bool or list:
        """This is the main function for every animal. It handles the movement, food and water search as well as mating and eating/drinking.

        Returns:
            bool or list: returns a list if mating has occurred or a bool based on if the animal is considered alive or dead
        """
        self.age += 1

        # mating cooldown
        if self.cooldown:
            if self.cooldown >= 100:
                self.cooldown = None
            else:
                self.cooldown += 1

        if not self.queued_movements:
            self.__normal_movement__()
        else:
            if (
                self.path_length
                and len(self.queued_movements) <= self.path_length / 2
                and self.path_length > 4
            ):
                # searches for a more optimal path to a moving target after half the path has been traversed
                self.queued_movements = ast.find_path(
                    self.map,
                    self.__convert_pos__(self.pos),
                    self.queued_movements[len(self.queued_movements) - 1],
                )
                self.path_length = len(self.queued_movements)
            self.__direct_movement__()

        # checks if either the food or water point has been reached
        if self.__convert_pos__(self.pos) == self.food_point:
            self.food_found = False
            self.food_point = None
            self.hunger -= 350 * (20 - self.hunger_rate)
        elif self.__convert_pos__(self.pos) == self.water_point:
            self.water_found = False
            self.water_point = None
            self.thirst -= 350 * (20 - self.thirst_rate)

        if self.mate:
            if not self.mate_pos:
                # this triggers only if a animal wants to mate with this animal
                self.mate.queued_movements.append(
                    self.__convert_pos__(self.pos))
                self.mate.mate_pos = self.__convert_pos__(self.pos)
            elif self.mate_pos == self.__convert_pos__(self.pos):
                return self.__mating_process__(self.genomes, self.mate.genomes)

        # increasing hunger and thirst
        self.hunger += self.hunger_rate
        self.thirst += self.thirst_rate

        if not self.queued_movements:
            self.__resolve_needs__()

        return self.hunger < 1000 and self.thirst < 1000 and self.age < self.max_age

    def __inside_range__(self, start: tuple, end: tuple, point: tuple) -> bool:
        """Checks if a point is inside the rectangle made by two points

        Args:
            start (tuple): top left corner of the rectangle
            end (tuple): bottom right corner of the rectangle
            point (tuple): point to check for

        Returns:
            bool: if point is inside true, else false
        """
        return (
            (point[0] >= start[0])
            and (point[0] <= end[1])
            and (point[1] >= start[1])
            and (point[1] <= end[1])
        )

    def __water_tile__(self, pos: tuple) -> bool:
        """Checks if a given point is a water tile.

        Args:
            pos (tuple): the tile which needs to get checked

        Returns:
            bool: if point is water true, else false
        """
        x, y = self.__convert_pos__(pos)[0], self.__convert_pos__(pos)[1]
        return self.map[y][x] == 5.0

    def __check_bounds__(self, direction: int) -> bool:
        """Checks if movement in a given direction would lead out of bounds

        Args:
            direction (int): the direction in which the animal wants to move

        Returns:
            bool: true if the move is valid, else false
        """
        if direction == 1 and self.pos[1] != 0:
            return True
        elif direction == 2 and self.pos[0] != 199 * TILESIZE:
            return True
        elif direction == 3 and self.pos[1] != 199 * TILESIZE:
            return True
        elif direction == 4 and self.pos[0] != 0:
            return True
        else:
            return False

    def __convert_pos__(self, pos: tuple) -> tuple:
        """Converts a given screen/map position into coordinates.

        Args:
            pos (tuple): position on the map/screen

        Returns:
            tuple: converted position
        """
        x = int(pos[0] / TILESIZE)
        y = int(pos[1] / TILESIZE)
        return x, y

    def __normal_movement__(self) -> None:
        """Normal/random movement function. Chooses a random direction and, if the move is valid, moves one space in that direction."""
        direction = rnd.randint(1, 4)

        if (
            direction == 1
            and self.__check_bounds__(direction)
            and not self.__water_tile__(tuple(np.subtract(self.pos, (0, TILESIZE))))
        ):  # Move Up
            self.rect.center -= pg.math.Vector2(0, TILESIZE)
            self.pos = tuple(np.subtract(self.pos, (0, TILESIZE)))
        elif (
            direction == 2
            and self.__check_bounds__(direction)
            and not self.__water_tile__(tuple(np.add(self.pos, (TILESIZE, 0))))
        ):  # Move Right
            self.rect.center += pg.math.Vector2(TILESIZE, 0)
            self.pos = tuple(np.add(self.pos, (TILESIZE, 0)))
        elif (
            direction == 3
            and self.__check_bounds__(direction)
            and not self.__water_tile__(tuple(np.add(self.pos, (0, TILESIZE))))
        ):  # Move Down
            self.rect.center += pg.math.Vector2(0, TILESIZE)
            self.pos = tuple(np.add(self.pos, (0, TILESIZE)))
        elif (
            direction == 4
            and self.__check_bounds__(direction)
            and not self.__water_tile__(tuple(np.subtract(self.pos, (0, TILESIZE))))
        ):  # Move Left
            self.rect.center -= pg.math.Vector2(TILESIZE, 0)
            self.pos = tuple(np.subtract(self.pos, (TILESIZE, 0)))

    def __direct_movement__(self) -> None:
        """Takes the first entry of the list of queued movements and places the animal on that position."""
        new_pos = self.queued_movements.pop(0)
        new_pos = new_pos[0] * TILESIZE, new_pos[1] * TILESIZE
        direction = tuple(np.subtract(self.pos, new_pos))
        self.rect.center -= pg.math.Vector2(direction[0], direction[1])
        self.pos = new_pos

    def __resolve_needs__(self) -> None:
        """Checks if the animal is hungry, thirsty or is able to mate and if so, triggers the corresponding functions."""
        if self.thirst > 500 and not self.water_found:
            self.__find_water__()
        elif self.hunger > 350 and not self.food_found:
            self.__find_food__()
        elif not self.mate and self.age > 100 and not self.cooldown:
            self.__find_mate__()

    def __find_prey__(self) -> None:
        """Checks if a huntable animal is in range, searches a path to it and changes the corresponding variables."""
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)

        for _ in range(41):
            # checking if the points are still in range and then
            # increasing the range of the search radius every iteration
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < 199:
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1] + 1)

            # iterating through all huntable animals
            for entry in self.huntable:
                prey_pos_conv = self.__convert_pos__(self.huntable[entry].pos)
                if (
                    self.__inside_range__(
                        start_point, end_point, prey_pos_conv)
                    and not self.huntable[entry].hunted
                ):
                    self.huntable[entry].hunted = True
                    self.huntable[entry].hunter = self
                    self.food_point = prey_pos_conv
                    self.food_found = True
                    self.prey = self.huntable[entry]
                    break

            if self.food_found:
                break

        if self.food_found:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.food_point
            )
            self.path_length = len(self.queued_movements)

    def __find_berry__(self) -> None:
        """Checks if a berry is in range, searches a path to it and changes the corresponding variables."""
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for _ in range(31):
            # checking if the points are still in range and then
            # increasing the range of the search radius every iteration
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < 199:
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1] + 1)

            for y in range(start_point[1], end_point[1]):
                for x in range(start_point[0], end_point[0]):
                    if self.map[y][x] == 0:  # checks for berry entry
                        self.food_found = True
                        self.food_point = (x, y)
                        break
                if self.food_found:
                    break

            if self.food_found:
                break

        if self.food_found:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.food_point
            )

    def __find_water__(self) -> None:
        """Checks if a water tile is in range, searches a path to it and changes the corresponding variables."""
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for _ in range(31):
            # checking if the points are still in range and then
            # increasing the range of the search radius every iteration
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < 199:
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1] + 1)

            for y in range(start_point[1], end_point[1]):
                for x in range(start_point[0], end_point[0]):
                    if self.map[y][x] == 5:  # checks for water entry
                        self.water_found = True
                        self.water_point = (x, y)
                        break
                if self.water_found:
                    break

            if self.water_found:
                break

        if self.water_found:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.water_point
            )

    def __find_mate__(self) -> None:
        """Checks if an appropriate animal is in range, searches a path to it and changes the corresponding variables."""
        start_point = self.__convert_pos__(self.pos)
        end_point = self.__convert_pos__(self.pos)
        for _ in range(31):
            if start_point[0] > 0:
                start_point = (start_point[0] - 1, start_point[1])
            if start_point[1] > 0:
                start_point = (start_point[0], start_point[1] - 1)
            if end_point[0] < 199:
                end_point = (end_point[0] + 1, end_point[1])
            if end_point[1] < 199:
                end_point = (end_point[0], end_point[1] + 1)

            for entry in self.population:
                mate_pos_conv = self.__convert_pos__(
                    self.population[entry].pos)
                # checks if the entry:
                # 1. is in range
                # 2. doesn't have a mate
                # 3. is not itself
                # 4. has reached mating age
                if (
                    self.__inside_range__(
                        start_point, end_point, mate_pos_conv)
                    and not self.population[entry].mate
                    and self.population[entry].key != self.key
                    and self.population[entry].age > 100
                ):
                    self.mate_pos = mate_pos_conv
                    self.population[entry].mate = self
                    self.mate = self.population[entry]
                    break

            if self.mate_pos:
                break

        if self.mate_pos:
            self.queued_movements = ast.find_path(
                self.map, self.__convert_pos__(self.pos), self.mate_pos
            )
            self.path_length = len(self.queued_movements)

    def __mating_process__(self, genomes1: dict, genomes2: dict) -> list:
        """Handles the mating process. Sets the corresponding variables and passes the genomes.

        Args:
            genomes1 (dict): genomes from animal 1
            genomes2 (dict): genomes from animal 2

        Returns:
            list: contains the animal type, the position and the new genomes
        """
        new_genomes = self.__generate_genoms__(genomes1, genomes2)
        self.cooldown = 1
        self.mate.cooldown = 1
        self.mate_pos = None
        self.mate.mate = None
        self.mate = None
        return [self.type, self.pos, new_genomes]

    def __generate_genoms__(self, genomes1: dict, genomes2: dict) -> dict:
        """Generates a new set of genomes based on the ones passed into the function.

        Args:
            genomes1 (dict): genomes from animal 1
            genomes2 (dict): genomes from animal 2

        Returns:
            dict: contains the genome values
        """
        genomes_f = genomes1
        genomes_m = genomes2

        inheritance_values = [0 for _ in range(6)]

        for i in range(0, 5, 2):
            t = rnd.randint(0, 1)
            r = rnd.randint(0, 3)
            if i == 0:  # age values
                if t == 0 and r >= 1:  # male dominant stays dominant
                    inheritance_values[i] = genomes_m["max_age_d"]
                    inheritance_values[i + 1] = genomes_f["max_age_r"]
                elif t == 0 and r == 0:  # male dominant becomes recessive
                    inheritance_values[i + 1] = genomes_m["max_age_d"]
                    inheritance_values[i] = genomes_f["max_age_r"]
                elif t == 1 and r >= 1:  # female dominant stays dominant
                    inheritance_values[i] = genomes_f["max_age_d"]
                    inheritance_values[i + 1] = genomes_m["max_age_r"]
                else:  # female dominant becomes recessive
                    inheritance_values[i + 1] = genomes_f["max_age_d"]
                    inheritance_values[i] = genomes_m["max_age_r"]
            elif i == 2:  # hunger values
                if t == 0 and r >= 1:  # male dominant stays dominant
                    inheritance_values[i] = genomes_m["hunger_rate_d"]
                    inheritance_values[i + 1] = genomes_f["hunger_rate_r"]
                elif t == 0 and r == 0:  # male dominant becomes recessive
                    inheritance_values[i + 1] = genomes_m["hunger_rate_d"]
                    inheritance_values[i] = genomes_f["hunger_rate_r"]
                else:  # female dominant stays dominant
                    inheritance_values[i] = genomes_f["hunger_rate_d"]
                    inheritance_values[i + 1] = genomes_m["hunger_rate_r"]
            # thirst values
            elif t == 0 and r >= 1:  # male dominant stays dominant
                inheritance_values[i] = genomes_m["thirst_rate_d"]
                inheritance_values[i + 1] = genomes_f["thirst_rate_r"]
            elif t == 0 and r == 0:  # male dominant becomes recessive
                inheritance_values[i + 1] = genomes_m["thirst_rate_d"]
                inheritance_values[i] = genomes_f["thirst_rate_r"]
            elif t == 1 and r >= 0:  # female dominant stays dominant
                inheritance_values[i] = genomes_f["thirst_rate_d"]
                inheritance_values[i + 1] = genomes_m["thirst_rate_r"]
            else:  # female dominant becomes recessive
                inheritance_values[i + 1] = genomes_f["thirst_rate_d"]
                inheritance_values[i] = genomes_m["thirst_rate_r"]

        if rnd.randint(1, 20) == 1:
            inheritance_values = self.__mutate_genes__(inheritance_values)

        return {
            "animal_type": genomes_m["animal_type"],
            "max_age_d": inheritance_values[0],
            "max_age_r": inheritance_values[1],
            "hunger_rate_d": inheritance_values[2],
            "hunger_rate_r": inheritance_values[3],
            "thirst_rate_d": inheritance_values[4],
            "thirst_rate_r": inheritance_values[5],
        }

    def __mutate_genes__(self, inh_val: list) -> list:
        """Mutation process of genomes.

        Args:
            inh_val (list): contains all inheritable values

        Returns:
            list: the changed inheritable values
        """
        new_values = inh_val

        for i in range(0, 5, 2):
            mut = round((rnd.uniform(new_values[i], new_values[i + 1]) / 4), 2)
            x = rnd.randint(0, 1)
            new_values[i] += mut if x == 0 else (-1) * mut
            new_values[i + 1] += mut if x == 0 else (-1) * mut

        return new_values
