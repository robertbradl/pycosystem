import pygame as pg
import random as rnd
import csv
from settings import *
from World.tile import Tile
from Animals.herbi import Herbivore
from Animals.carni import Carnivore
from Animals.omni import Omnivore


class World:

    def __init__(self) -> None:

        # grab display surface
        self.display_surface = pg.display.get_surface()

        self.world_sprites = pg.sprite.Group()
        self.alive_sprites = pg.sprite.Group()
        self.dead_sprites = pg.sprite.Group()
        self.map = []

        # dictionaries containing all alive instances of their respective animal type
        self.herbis = {}
        self.carnis = {}
        self.omnis = {}

        # key values corresponding to the dictionaries
        self.herb_key = 1
        self.carn_key = 1
        self.omnis_key = 1

        # paths to all the sprites
        self.images = {
            'grass': 'World/tileset/grass.png',
            'berry': 'World/tileset/berry.png',
            'water': 'World/tileset/water.png',
            'herbi': 'World/tileset/herbi.png',
            'carni': 'World/tileset/carni.png',
            'omni': 'World/tileset/omni.png',
        }

        # map setup
        self.__create_map__()



############## MAKE ANIMAL SECTION

# all functions work identical: take a position and, depending if genomns 
# were passed or not, either generate a set of genomns or just pass the 
# given genomns into the corresponding constructor

    def __make_carnivore__(self, pos: tuple, passed_genoms: dict = None) -> None:
        if passed_genoms:
            self.carnis[self.carn_key] = Carnivore(
                pos, self.herbis, passed_genoms, self.carnis, self.map, self.carn_key, self.images['carni'], [self.alive_sprites])
        else:
            genoms = {'animal_type': 'carni',
                  'max_age_d': rnd.randint(700, 800),
                  'max_age_r': rnd.randint(700, 800),
                  'hunger_rate_d': round(rnd.uniform(0.6, 1.4),2),
                  'hunger_rate_r': round(rnd.uniform(0.6, 1.4),2),
                  'thirst_rate_d': round(rnd.uniform(0.6, 1.4),2),
                  'thirst_rate_r': round(rnd.uniform(0.6, 1.4),2)}
            
            self.carnis[self.carn_key] = Carnivore(
                pos, self.herbis, genoms, self.carnis, self.map, self.carn_key, self.images['carni'], [self.alive_sprites])

        self.carn_key += 1

    def __make_herbivore__(self, pos: tuple, passed_genoms: dict = None) -> None:
        if passed_genoms:
            self.herbis[self.herb_key] = Herbivore(
                pos, passed_genoms, self.herbis, self.map, self.herb_key, self.images['herbi'], [self.alive_sprites])
        else:
            genoms = {'animal_type': 'herbi',
                  'max_age_d': rnd.randint(500, 600),
                  'max_age_r': rnd.randint(500, 600),
                  'hunger_rate_d': round(rnd.uniform(0.3, 0.8),2),
                  'hunger_rate_r': round(rnd.uniform(0.3, 0.8),2),
                  'thirst_rate_d': round(rnd.uniform(0.3, 0.8),2),
                  'thirst_rate_r': round(rnd.uniform(0.3, 0.8),2)}
            
            self.herbis[self.herb_key] = Herbivore(
                pos, genoms, self.herbis, self.map, self.herb_key, self.images['herbi'], [self.alive_sprites])

        self.herb_key += 1

    def __make_omnivore__(self, pos: tuple, passed_genoms: dict = None) -> None:
        if passed_genoms:
            self.omnis[self.omnis_key] = Omnivore(
                pos, self.herbis, passed_genoms, self.omnis, self.map, self.omnis_key, self.images['omni'], [self.alive_sprites])
        else:
            genoms = {'animal_type': 'omni',
                  'max_age_d': rnd.randint(900, 1000),
                  'max_age_r': rnd.randint(900, 1000),
                  'hunger_rate_d': round(rnd.uniform(0.3, 0.8),2),
                  'hunger_rate_r': round(rnd.uniform(0.3, 0.8),2),
                  'thirst_rate_d': round(rnd.uniform(0.3, 0.8),2),
                  'thirst_rate_r': round(rnd.uniform(0.3, 0.8),2)}
            
            self.omnis[self.omnis_key] = Omnivore(
                pos, self.herbis, genoms, self.omnis, self.map, self.omnis_key, self.images['omni'], [self.alive_sprites])

        self.omnis_key += 1

############## END OF MAKE ANIMAL SECTION



    def __create_map__(self) -> None:

        # reading map contents
        with open("World/map_random.csv") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
            for row in reader:
                self.map.append(row)

        # converts CSV to positions and draws the corresponding tile
        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 2.0: # grass tiles
                    Tile((x, y), self.images['grass'], [self.world_sprites])
                elif col == 0.0: # berry tiles
                    Tile((x, y), self.images['berry'], [self.world_sprites])
                elif col == 5.0: # water tiles
                    Tile((x, y), self.images['water'], [self.world_sprites])
                elif col == 1.0: # carnivore
                    # there needs to be a grass tile placed under the animal
                    Tile((x, y), self.images['grass'], [self.world_sprites])
                    self.__make_carnivore__((x, y))
                elif col == 3.0: # herbivore
                    # see above
                    Tile((x, y), self.images['grass'], [self.world_sprites])
                    self.__make_herbivore__((x, y))
                elif col == 4.0: # omnivore
                    Tile((x, y), self.images['grass'], [self.world_sprites])
                    self.__make_omnivore__((x,y))
                else:  # this shouldn't happen
                    print("Error: Unknown value in CSV at: " +
                          str((x, y)) + ". Exiting program.")
                    exit(1)

    def run(self) -> None:
        # updating the sprites
        self.world_sprites.draw(self.display_surface)
        self.alive_sprites.draw(self.display_surface)

        # removing all dead sprites
        for sprite in self.dead_sprites:
            sprite.kill()

        # alive check and process for every sprite/animal
        for animal in self.alive_sprites:
            value = animal.alive() 
            # alive function returns either a boolean or a list if the animal mated
            if type(value) == bool:
                # check if alive or dead
                if not value:
                    self.dead_sprites.add(animal)
                    self.alive_sprites.remove(animal)
                    if animal.type == 'herbi':
                        self.herbis.pop(animal.key)
                    elif animal.type == 'carni':
                        self.carnis.pop(animal.key)
                    elif animal.type == 'omni':
                        self.omnis.pop(animal.key)
                    else:  # this shouldn't happen
                        print(
                            "Error: Animal of unknown type encountered during removal process. Exiting programm.")
                        exit(1)
            else:
                # if the animal mated
                if value[0] == 'herbi':
                    self.__make_herbivore__(value[1], value[2])
                elif value[0] == 'carni':
                    self.__make_carnivore__(value[1], value[2])
                elif value[0] == 'omni':
                    self.__make_omnivore__(value[1], value[2])
                else:  # this shouldn't happen
                    print(
                        "Error: Animal of unknown type encountered during creation process. Exiting programm.")
                    exit(1)