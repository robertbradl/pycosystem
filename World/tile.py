import pygame as pg
from settings import *


class Tile(pg.sprite.Sprite):

    # general setup
    def __init__(self, pos: tuple, path: str, groups) -> None:
        super().__init__(groups)
        self.image = pg.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
