import pygame as pg
from settings import *
from World.world import World


class Simulation:

    def __init__(self) -> None:
        """Initializes the Simulation object with necessary setup."""
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Pycosystem")
        self.clock = pg.time.Clock()

        self.world = World()
        self.r_state = True  # run state for pause button

        self.font = pg.font.SysFont("arial", 20, True)

        # button colors
        self.light_color = (183, 192, 154)
        self.dark_color = (127, 133, 109)

        self.b1_texts = ["Pause", "Unpause"]
        self.animal_event = pg.USEREVENT + 1

    def run(self) -> None:
        """Runs the simulation process."""
        pg.time.set_timer(
            self.animal_event, int(1000 / SPEED)
        )  # timer for animal events
        run = True
        while run:
            mouse = pg.mouse.get_pos()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if (
                        WIDTH / 2 - 100 <= mouse[0] <= WIDTH / 2 + 100
                        and HEIGHT - 75 <= mouse[1] <= HEIGHT - 25
                    ):  # button 1
                        self.r_state = not self.r_state
                elif event.type == self.animal_event:
                    self.world.run(self.r_state, True)

            self.screen.fill("black")
            self.world.run(self.r_state, False)
            self.__buttons__()

            pg.display.update()
            self.clock.tick(FPS)

        pg.quit()

    def __buttons__(self) -> None:
        """Draws all buttons."""
        mouse = pg.mouse.get_pos()

        # color for pause/unpause button
        if (
            WIDTH / 2 - 100 <= mouse[0] <= WIDTH / 2 + 100
            and HEIGHT - 75 <= mouse[1] <= HEIGHT - 25
        ):
            button1 = pg.draw.rect(
                self.screen, self.light_color, [WIDTH / 2 - 100, HEIGHT - 75, 200, 50]
            )
        else:
            button1 = pg.draw.rect(
                self.screen, self.dark_color, [WIDTH / 2 - 100, HEIGHT - 75, 200, 50]
            )

        # text for pause/unpause button (button1)
        if self.r_state:
            b1_text = self.font.render(self.b1_texts[0], True, (0, 0, 0))
        else:
            b1_text = self.font.render(self.b1_texts[1], True, (0, 0, 0))

        b1_rect = b1_text.get_rect(center=(button1.centerx, button1.centery))
        self.screen.blit(b1_text, b1_rect)


if __name__ == "__main__":
    """test"""
    simulation = Simulation()
    simulation.run()
