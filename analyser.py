import pygame as pg
import matplotlib.pyplot as plt
import numpy as np

class Analyser:
    def __init__(self) -> None:
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode((200,200))
        pg.display.set_caption("Analyser")
        self.clock = pg.time.Clock()

    def run(self) -> None:
        plt.ion()
        fig, axs = plt.subplots(3,3)

        
        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
            for y in range(3):
                for x in range(3):
                    y_val = np.random.random([10,1])
                    axs[y,x].plot(y_val)
                    axs[y,x].set_title(f'Axis [{y},{x}]')
            for ax in axs.flat:
                ax.set(xlabel='x-label', ylabel='y-label')
                ax.label_outer()

            plt.draw()
            plt.pause(1)
            for ax in axs:
                for pl in ax:
                    pl.cla()



if __name__ == "__main__":
    analyser = Analyser()
    analyser.run()