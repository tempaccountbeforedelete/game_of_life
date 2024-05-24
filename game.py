import pygame as pg
import numpy as np
import time
import constant as g_cst


class GameEngine:
    def __init__(self, WINDOW_SIZE=(800, 600)):
        pg.init()
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.cells = np.zeros((60, 80))
        self.pixel_size = 10

    def update(self, screen, cells, pixel_size, launch_sim=False):
        next_grid = np.zeros_like(cells)

        for row, col in np.ndindex(cells.shape):
            neighbor_cells = (
                np.sum(cells[row - 1 : row + 2, col - 1 : col + 2]) - cells[row, col]
            )
            color = g_cst.BACKGROUND if cells[row, col] == 0 else g_cst.ALIVE_CELL

            if cells[row, col] == 1:
                if neighbor_cells < 2 or neighbor_cells > 3:  # alone or too many
                    if launch_sim:
                        color = g_cst.DEAD_CELL

                if 2 <= neighbor_cells <= 3:
                    if launch_sim:
                        next_grid[row, col] = 1
                        color = g_cst.ALIVE_CELL

            else:
                if neighbor_cells == 3:
                    if launch_sim:
                        next_grid[row, col] = 1
                        color = g_cst.ALIVE_CELL

            pg.draw.rect(
                screen,
                color,
                (
                    col * pixel_size,
                    row * pixel_size,
                    pixel_size - 1,
                    pixel_size - 1,
                ),
            )
        return next_grid

    def run(self):
        pg.init()
        self.screen.fill(g_cst.GRID_COLOR)
        self.update(self.screen, self.cells, self.pixel_size)
        pg.display.flip()
        pg.display.update()

        run_simulation = False

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return

                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        run_simulation = not run_simulation
                        self.update(self.screen, self.cells, self.pixel_size)
                        pg.display.update()

                if pg.mouse.get_pressed()[0]:
                    position = pg.mouse.get_pos()
                    self.cells[
                        position[1] // self.pixel_size, position[0] // self.pixel_size
                    ] = 1
                    self.update(self.screen, self.cells, self.pixel_size)
                    pg.display.update()

            self.screen.fill(g_cst.GRID_COLOR)

            if run_simulation:
                self.cells = self.update(self.screen, self.cells, self.pixel_size, True)
                pg.display.update()

            time.sleep(0.001)
