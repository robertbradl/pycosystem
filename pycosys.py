import pygame as pg
import sys
from settings import *
from World.world import World

class Simulation:

    # general setup
    def __init__(self) -> None:
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption('Pycosystem')
        self.clock = pg.time.Clock()

        self.world = World()

    # run process
    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            
            self.screen.fill('black')
            self.world.run()
            pg.display.update()
            self.clock.tick(SPEED)


if __name__ == '__main__':
    simulation = Simulation()
    simulation.run()