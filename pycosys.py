import pygame as pg
import sys
from settings import *
from World.world import World


class Simulation:
    # general setup
    def __init__(self) -> None:
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Pycosystem")
        self.clock = pg.time.Clock()

        self.world = World()
        self.r_state = True

        self.font = pg.font.SysFont("arial", 20, True)
        self.light_color = (183,192,154)
        self.dark_color = (127,133,109)
        self.b1_texts = ["Pause", "Unpause"]

    # run process
    def run(self) -> None:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
# sourcery skip: merge-nested-ifs
                if event.type == pg.MOUSEBUTTONDOWN:
                    if WIDTH/2-100 <= mouse[0] <= WIDTH/2+100 and HEIGHT-75 <= mouse[1] <= HEIGHT-25: # button 1
                        self.r_state = not self.r_state


            self.screen.fill("black")
            
            self.world.run(self.r_state)

            mouse = pg.mouse.get_pos()

            if WIDTH/2-100 <= mouse[0] <= WIDTH/2+100 and HEIGHT-75 <= mouse[1] <= HEIGHT-25:
                button1 = pg.draw.rect(self.screen,self.light_color,[WIDTH/2-100,HEIGHT-75,200,50])
            else:
                button1 = pg.draw.rect(self.screen,self.dark_color,[WIDTH/2-100,HEIGHT-75,200,50])
            if self.r_state:
                b1_text = self.font.render(self.b1_texts[0], True, (0,0,0))
            else:
                b1_text = self.font.render(self.b1_texts[1], True, (0,0,0))
            b1_rect = b1_text.get_rect(center = (button1.centerx,button1.centery))
            self.screen.blit(b1_text,b1_rect)
            
            pg.display.update()
            self.clock.tick(SPEED)


if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
