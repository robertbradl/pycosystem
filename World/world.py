import pygame as pg
import random as rnd
from settings import *
from World.tile import Tile
from Animals.herbi import Herbivore
from Animals.carni import Carnivore
from Animals.omni import Omnivore
from generator import generate_map


class World:
    """Handles the actual simulated world"""

    def __init__(self, map: list = None) -> None:
        """Initializes the World object with necessary setup.

        Args:
            map (list): Optional parameter for the map configuration.
        """
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.SysFont("arial", 20, True)

        self.world_sprites = pg.sprite.Group()
        self.alive_sprites = pg.sprite.Group()
        self.dead_sprites = pg.sprite.Group()

        self.map = generate_map() if map is None else map

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
            "grass": "World/tileset/grass.png",
            "berry": "World/tileset/berry.png",
            "water": "World/tileset/water.png",
            "herbi": "World/tileset/herbi.png",
            "carni": "World/tileset/carni.png",
            "omni": "World/tileset/omni.png",
        }

        # map setup
        self.__create_map__()

    # MAKE ANIMAL SECTION

    def __make_carnivore__(self, pos: tuple, passed_genomes: dict = None) -> None:
        """Creates a new carnivore with either a random or a passed set of genomes.

        Args:
            pos (tuple): The position at which the animal will be spawned in.
            passed_genomes (dict, optional): Passed on genomes in case of mating. Defaults to None so that if no genomes are passed, a random set gets generated.
        """
        if passed_genomes:
            self.carnis[self.carn_key] = Carnivore(
                pos,
                self.herbis,
                passed_genomes,
                self.carnis,
                self.map,
                self.carn_key,
                self.images["carni"],
                [self.alive_sprites],
            )
        else:
            genomes = {
                "animal_type": "carni",
                "max_age_d": rnd.randint(700, 800),
                "max_age_r": rnd.randint(700, 800),
                "hunger_rate_d": round(rnd.uniform(8, 15), 2),
                "hunger_rate_r": round(rnd.uniform(8, 15), 2),
                "thirst_rate_d": round(rnd.uniform(8, 15), 2),
                "thirst_rate_r": round(rnd.uniform(8, 15), 2),
            }

            self.carnis[self.carn_key] = Carnivore(
                pos,
                self.herbis,
                genomes,
                self.carnis,
                self.map,
                self.carn_key,
                self.images["carni"],
                [self.alive_sprites],
            )

        self.carn_key += 1

    def __make_herbivore__(self, pos: tuple, passed_genomes: dict = None) -> None:
        """Creates a new herbivore with either a random or a passed set of genomes.

        Args:
            pos (tuple): The position at which the animal will be spawned in.
            passed_genomes (dict, optional): Passed on genomes in case of mating. Defaults to None so that if no genomes are passed, a random set gets generated.
        """
        if passed_genomes:
            self.herbis[self.herb_key] = Herbivore(
                pos,
                passed_genomes,
                self.herbis,
                self.map,
                self.herb_key,
                self.images["herbi"],
                [self.alive_sprites],
            )
        else:
            genomes = {
                "animal_type": "herbi",
                "max_age_d": rnd.randint(500, 600),
                "max_age_r": rnd.randint(500, 600),
                "hunger_rate_d": round(rnd.uniform(5, 10), 2),
                "hunger_rate_r": round(rnd.uniform(5, 10), 2),
                "thirst_rate_d": round(rnd.uniform(5, 10), 2),
                "thirst_rate_r": round(rnd.uniform(5, 10), 2),
            }

            self.herbis[self.herb_key] = Herbivore(
                pos,
                genomes,
                self.herbis,
                self.map,
                self.herb_key,
                self.images["herbi"],
                [self.alive_sprites],
            )

        self.herb_key += 1

    def __make_omnivore__(self, pos: tuple, passed_genomes: dict = None) -> None:
        """Creates a new omnivore with either a random or a passed set of genomes.

        Args:
            pos (tuple): The position at which the animal will be spawned in.
            passed_genomes (dict, optional): Passed on genomes in case of mating. Defaults to None so that if no genomes are passed, a random set gets generated.
        """
        if passed_genomes:
            self.omnis[self.omnis_key] = Omnivore(
                pos,
                self.herbis,
                passed_genomes,
                self.omnis,
                self.map,
                self.omnis_key,
                self.images["omni"],
                [self.alive_sprites],
            )
        else:
            genomes = {
                "animal_type": "omni",
                "max_age_d": rnd.randint(900, 1000),
                "max_age_r": rnd.randint(900, 1000),
                "hunger_rate_d": round(rnd.uniform(8, 15), 2),
                "hunger_rate_r": round(rnd.uniform(8, 15), 2),
                "thirst_rate_d": round(rnd.uniform(8, 15), 2),
                "thirst_rate_r": round(rnd.uniform(8, 15), 2),
            }

            self.omnis[self.omnis_key] = Omnivore(
                pos,
                self.herbis,
                genomes,
                self.omnis,
                self.map,
                self.omnis_key,
                self.images["omni"],
                [self.alive_sprites],
            )

        self.omnis_key += 1

    # END OF MAKE ANIMAL SECTION

    def __create_map__(self) -> None:
        """Creates the map from the array the generator module created."""

        # converts array to positions and draws the corresponding tile
        for row_index, row in enumerate(self.map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 2.0:  # grass tiles
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                elif col == 0.0:  # berry tiles
                    # there needs to be a grass tile placed under the berry bush
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    Tile((x, y), self.images["berry"], [self.world_sprites])
                elif col == 5.0:  # water tiles
                    Tile((x, y), self.images["water"], [self.world_sprites])
                elif col == 1.0:  # carnivore
                    # there needs to be a grass tile placed under the animal
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    self.__make_carnivore__((x, y))
                elif col == 3.0:  # herbivore
                    # see above
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    self.__make_herbivore__((x, y))
                elif col == 4.0:  # omnivore
                    Tile((x, y), self.images["grass"], [self.world_sprites])
                    self.__make_omnivore__((x, y))
                else:  # this shouldn't happen
                    print(
                        f"Error: Unknown value in array at: {(x, y)}. Exiting program."
                    )
                    exit(1)

    def __update_graphics__(self) -> None:
        """Updates the sprites on screen and the animal counters."""
        self.world_sprites.draw(self.display_surface)
        self.alive_sprites.draw(self.display_surface)

        live_herbs = self.font.render(
            f"Alive herbivores: {len(self.herbis)}", True, (255, 255, 255)
        )
        live_carns = self.font.render(
            f"Alive carnivores:  {len(self.carnis)}", True, (255, 255, 255)
        )
        live_ommnis = self.font.render(
            f"Alive omnivores:  {len(self.omnis)}", True, (255, 255, 255)
        )
        self.display_surface.blit(live_herbs, (10, 1015))
        self.display_surface.blit(live_carns, (10, 1040))
        self.display_surface.blit(live_ommnis, (10, 1065))

    def __remove_animal(self, animal) -> None:
        """Removes the specified animal from the corresponding animal type dictionary and kills the animal.

        Args:
            animal: The animal to be removed.
        """
        if animal.type == "herbi":
            self.herbis.pop(animal.key)
        elif animal.type == "carni":
            self.carnis.pop(animal.key)
        elif animal.type == "omni":
            self.omnis.pop(animal.key)
        else:  # this shouldn't happen
            print(
                "Error: Animal of unknown type encountered during removal process. Exiting program."
            )
            exit(1)
        animal.kill()  # removes sprite from all groups

    def __handle_mating__(self, genomes: list) -> None:
        """Handles the mating process based on the given genomes to create specific types of animals.

        Args:
            genomes (list): List containing genetic information for mating.
        """
        if genomes[0] == "herbi":
            self.__make_herbivore__(genomes[1], genomes[2])
        elif genomes[0] == "carni":
            self.__make_carnivore__(genomes[1], genomes[2])
        elif genomes[0] == "omni":
            self.__make_omnivore__(genomes[1], genomes[2])
        else:  # this shouldn't happen
            print(
                "Error: Animal of unknown type encountered during creation process. Exiting program."
            )
            exit(1)

    def run(self, r_state: bool, t_state: bool) -> None:
        """Runs the simulation, meaning this function updates the map, triggers the alive function of every animal and acts accordingly.

        Args:
            r_state (bool): The current run_state of the simulation. If the simulation is paused, this is False.
            t_state (bool): The current trigger of the simulation. If no event-trigger has happed in the current iteration, this is False.
        """

        self.__update_graphics__()

        if not (r_state and t_state):
            return
        for animal in self.alive_sprites:
            value = animal.alive()
            # alive function returns either a boolean or a list if the animal mated
            if type(value) == bool:
                # check if alive or dead
                if not value:
                    self.__remove_animal(animal)
            else:
                self.__handle_mating__(value)
