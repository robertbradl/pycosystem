import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):

    def __init__(self, pos: tuple, path: str, groups) -> None:
        """Initializes a Tile object with a specific image at a given position.

        Args:
            pos (tuple): The position of the Tile.
            path (str): The path to the image file.
            groups: The sprite groups the Tile belongs to.
        """
        super().__init__(groups)
        self.image = pg.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
