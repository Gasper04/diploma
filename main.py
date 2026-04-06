
import random

from cube.cube import Cube
from cube.scramble import generate_scramble
from solvers.classic.classic_solver import ClassicSolver
from display.viewer import Viewer


seed = random.randint(1, 1000)
size = 0
size = int(input("select the size of cube:"))

cube = Cube(size)
scramble = generate_scramble(size, relative_length=1, seed=seed)
viewer = Viewer(cube)
viewer.show()
viewer.update()
cube.apply_sequence_display(scramble, viewer, delay=0)

input("Cube is scrambled, press Enter to solve")
solver = ClassicSolver(cube)
solution = solver.solve()
cube.apply_sequence_display(solution, viewer, delay=0)

input("Press Enter to end the program")

