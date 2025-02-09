from tkinter import Tk, BOTH, Canvas


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point_1: Point, point_2: Point):
        self.point_1: Point = point_1
        self.point_2: Point = point_2

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.point_1.x,
            self.point_1.y,
            self.point_2.x,
            self.point_2.y,
            fill=fill_color,
            width=2,
        )


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.root_widget = Tk()
        self.root_widget.title = "MazeSolver"
        self.canvas = Canvas(self.root_widget, width=width, height=height)
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.root_widget.update_idletasks()
        self.root_widget.update()

    def wait_for_close(self):
        self.running = True
        while self.running == True:
            self.redraw()

    def close(self):
        self.running = False
        self.root_widget.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(
        self,
        point_1: Point,
        point_2: Point,
        window: Window,
        has_left_wall=True,
        has_right_wall=True,
        has_top_wall=True,
        has_bottom_wall=True,
    ):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.visited = False
        self._x1 = point_1.x
        self._x2 = point_2.x
        self._y1 = point_1.y
        self._y2 = point_2.y
        self._midpoint = self._calculate_midpoint()
        self._win = window

    def draw(self):
        top_left = Point(self._x1, self._y1)
        bottom_left = Point(self._x1, self._y2)
        top_right = Point(self._x2, self._y1)
        bottom_right = Point(self._x2, self._y2)

        if self.has_left_wall:
            left_line = Line(top_left, bottom_left)
            left_line.draw(self._win.canvas, "black")
        else:
            left_line = Line(top_left, bottom_left)
            left_line.draw(self._win.canvas, "#d9d9d9")
        if self.has_top_wall:
            top_line = Line(top_left, top_right)
            top_line.draw(self._win.canvas, "black")
        else:
            top_line = Line(top_left, top_right)
            top_line.draw(self._win.canvas, "#d9d9d9")
        if self.has_bottom_wall:
            bottom_line = Line(bottom_left, bottom_right)
            bottom_line.draw(self._win.canvas, "black")
        else:
            bottom_line = Line(bottom_left, bottom_right)
            bottom_line.draw(self._win.canvas, "#d9d9d9")
        if self.has_right_wall:
            right_line = Line(top_right, bottom_right)
            right_line.draw(self._win.canvas, "black")
        else:
            right_line = Line(top_right, bottom_right)
            right_line.draw(self._win.canvas, "#d9d9d9")

    def _calculate_midpoint(self):
        mid_x = (self._x2 + self._x1) // 2
        mid_y = (self._y2 + self._y1) // 2
        return Point(mid_x, mid_y)

    def draw_move(self, to_cell, undo=False):  # type: ignore
        color = "red"
        if undo:
            color = "gray"
        line = Line(self._midpoint, to_cell._midpoint)
        line.draw(self._win.canvas, color)
