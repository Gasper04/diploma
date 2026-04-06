from cube.cube import Cube
from cube.sequence import Sequence

from solvers.helpers.orient import orient
from solvers.classic.centers import solve_centers
from solvers.classic.edges import EdgePieceSolver
from solvers.classic.beginner.white_cross import WhiteCrossSolver
from solvers.classic.beginner.white_corners import WhiteCornersSolver
from solvers.classic.beginner.second_layer import SecondLayerSolver
from solvers.classic.beginner.yellow_cross import YellowCrossSolver
from solvers.classic.beginner.orient_yellow_corners import YellowCornersOrient
from solvers.classic.beginner.solve_yellow_corners import YellowCornersSolver
from solvers.classic.beginner.solve_yellow_edges import YellowEdgesSolver


class ClassicSolver:
    def __init__(self, cube: Cube):
        self.cube = cube

    def solve(self) -> Sequence:
        _cube = self.cube.copy()
        solution = Sequence()

        # For 3x3 cubes, just orient the cube
        if _cube.n == 3:
            moves = orient(_cube)
            _cube.apply_sequence(moves)
            solution.extend(moves)
        else:
            # Solve centers and edges for cubes larger than 3x3
            centers_solution = solve_centers(_cube)
            _cube.apply_sequence(centers_solution)
            solution.extend(centers_solution)

            edges_solution = EdgePieceSolver(_cube).solve_edges()
            _cube.apply_sequence(edges_solution)
            solution.extend(edges_solution)

        # Solve the rest (white cross, corners, second layer, yellow layer)
        wcs = WhiteCrossSolver(_cube)
        moves = wcs.solve_white_cross()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        wcrs = WhiteCornersSolver(_cube)
        moves = wcrs.solve_white_corners()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        sls = SecondLayerSolver(_cube)
        moves = sls.solve_second_layer()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        ycs = YellowCrossSolver(_cube)
        moves = ycs.solve_yellow_cross()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        yco = YellowCornersOrient(_cube)
        moves = yco.orient_yellow_corners()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        ycs2 = YellowCornersSolver(_cube)
        moves = ycs2.solve_yellow_corners()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        yes = YellowEdgesSolver(_cube)
        moves = yes.solve_yellow_edges()
        _cube.apply_sequence(moves)
        solution.extend(moves)

        # Final orientation to match standard cube position
        moves = orient(_cube)
        _cube.apply_sequence(moves)
        solution.extend(moves)

        return solution