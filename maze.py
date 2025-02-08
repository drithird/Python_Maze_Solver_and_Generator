from visuals import Cell, Point
import time


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = self._create_cells()
        self._draw_cells()
        self._break_entrance_and_exit()

    def _create_cells(self):
        grid = []
        current_x = self._x1
        current_y = self._y1
        for row in range(self._num_rows):
            cols = []
            current_x = self._x1
            for col in range(self._num_cols):
                point1 = Point(current_x, current_y)
                point2 = Point(
                    current_x + self._cell_size_x, current_y + self._cell_size_y
                )
                cell = Cell(point1, point2, self._win)
                cols.append(cell)
                current_x += self._cell_size_x

            grid.append(cols)
            current_y += self._cell_size_y
        return grid

    def _break_entrance_and_exit(self):
        entrance: Cell = self._cells[0][0]
        ext: Cell = self._cells[self._num_rows - 1][self._num_cols - 1]
        entrance.has_top_wall = False
        ext.has_bottom_wall = False
        entrance.draw()
        ext.draw()

    def _draw_cells(self):
        if self._win is None:
            return
        for row in self._cells:
            for cell in row:
                cell.draw()
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(5)
