from visuals import Window
from maze import Maze

win = Window(1000, 1000)
maze = Maze(10, 10, 20, 20, 30, 30, win)
maze.solve()
win.wait_for_close()
