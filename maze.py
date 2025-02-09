from visuals import Cell, Point
import time
import random


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
        random.seed()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def solve(self):
        self._solve_r(0, 0)

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
        time.sleep(0.05)

    def _break_walls_r(self, i, j):
        start: Cell = self._cells[i][j]
        start.visited = True
        while True:
            to_visit = []
            if 0 <= i + 1 < self._num_rows and 0 <= j < self._num_cols:
                cell: Cell = self._cells[i + 1][j]
                if not cell.visited:
                    to_visit.append((i + 1, j))
            if 0 <= i < self._num_rows and 0 <= j + 1 < self._num_cols:
                cell: Cell = self._cells[i][j + 1]
                if not cell.visited:
                    to_visit.append((i, j + 1))
            if 0 <= i - 1 < self._num_rows and 0 <= j < self._num_cols:
                cell: Cell = self._cells[i - 1][j]
                if not cell.visited:
                    to_visit.append((i - 1, j))
            if 0 <= i < self._num_rows and 0 <= j - 1 < self._num_cols:
                cell: Cell = self._cells[i][j - 1]
                if not cell.visited:
                    to_visit.append((i, j - 1))
            if not to_visit:
                return
            cell_chosen = to_visit[random.randint(0, len(to_visit) - 1)]
            if cell_chosen[0] < i and cell_chosen[1] == j:
                # If the cell to the top is chosen
                start.has_top_wall = False
                start.draw()
                self._cells[cell_chosen[0]][cell_chosen[1]].has_bottom_wall = False
                self._cells[cell_chosen[0]][cell_chosen[1]].draw()
                self._animate()
                self._break_walls_r(cell_chosen[0], cell_chosen[1])
            elif cell_chosen[0] > i and cell_chosen[1] == j:
                # If the cell to the bottom is chosen
                end = self._cells[cell_chosen[0]][cell_chosen[1]]
                start.has_bottom_wall = False
                start.draw()
                end.has_top_wall = False
                end.draw()
                self._animate()
                self._break_walls_r(cell_chosen[0], cell_chosen[1])
            elif cell_chosen[0] == i and cell_chosen[1] > j:
                # If the cell to the right is chosen
                start.has_right_wall = False
                start.draw()
                self._cells[cell_chosen[0]][cell_chosen[1]].has_left_wall = False
                self._cells[cell_chosen[0]][cell_chosen[1]].draw()
                self._animate()
                self._break_walls_r(cell_chosen[0], cell_chosen[1])
            elif cell_chosen[0] == i and cell_chosen[1] < j:
                # If the cell to the left is chosen
                start.has_left_wall = False
                start.draw()
                self._cells[cell_chosen[0]][cell_chosen[1]].has_right_wall = False
                self._cells[cell_chosen[0]][cell_chosen[1]].draw()
                self._animate()
                self._break_walls_r(cell_chosen[0], cell_chosen[1])

    def _reset_cells_visited(self):
        for row in self._cells:
            for cell in row:
                cell.visited = False

    def _solve_r(self, i=0, j=0):
        current_location = (i, j)
        end = (self._num_rows - 1, self._num_cols - 1)
        self._animate()
        current_cell: Cell = self._cells[current_location[0]][current_location[1]]
        current_cell.visited = True
        if current_location[0] == end[0] and current_location[1] == end[1]:
            return True
        direction = ["right", "down", "left", "up"]
        for choice in direction:
            print(current_location, f"Trying to move {choice}")
            if (
                choice == "right"
                and 0 <= j + 1 < self._num_cols
                and current_cell.has_right_wall == False
                and self._cells[i][j + 1].visited == False
            ):
                print(current_location, current_cell.has_right_wall)
                next_cell = self._cells[i][j + 1]
                current_cell.draw_move(next_cell)
                if self._solve_r(i, j + 1):
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)
            if (
                choice == "down"
                and 0 <= i + 1 < self._num_rows
                and current_cell.has_bottom_wall == False
                and self._cells[i + 1][j].visited == False
            ):
                next_cell = self._cells[i + 1][j]
                current_cell.draw_move(next_cell)
                if self._solve_r(i + 1, j):
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)
            if (
                choice == "left"
                and 0 <= j - 1 < self._num_cols
                and current_cell.has_left_wall == False
                and self._cells[i][j - 1].visited == False
            ):
                next_cell = self._cells[i][j - 1]
                current_cell.draw_move(next_cell)
                if self._solve_r(i, j - 1):
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)
            if (
                choice == "up"
                and 0 <= i - 1 < self._num_rows
                and current_cell.has_top_wall == False
                and self._cells[i - 1][j].visited == False
            ):
                next_cell = self._cells[i - 1][j]
                current_cell.draw_move(next_cell)
                if self._solve_r(i - 1, j):
                    return True
                else:
                    current_cell.draw_move(next_cell, undo=True)
        return False
