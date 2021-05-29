import numpy as np


UNIT_HEX_XA = np.array([1.0, 0.0, 0.0])
UNIT_HEX_XB = np.array([0.5, np.sqrt(3) / 2, 0.0])

UNIT_HEX_YA = np.array([0.0, 1.0, 0.0])
UNIT_HEX_YB = np.array([np.sqrt(3) / 2, 0.5, 0.0])

UNIT_X = np.array([1.0, 0.0, 0.0])
UNIT_Y = np.array([0.0, 1.0, 0.0])


def init(spacing, N, unitA, unitB):
    grid = []
    for A in np.arange(-N, N + 1, 1):
        for B in np.arange(-N, N + 1, 1):
            grid.append(spacing * (A * unitA + B * unitB))
    return np.array(grid)


def init_hexagonal(spacing, N):
    return init(
        spacing=spacing,
        N=N,
        unitA=UNIT_HEX_XA,
        unitB=UNIT_HEX_XB,
    )


def init_square(spacing, N):
    return init(
        spacing=spacing,
        N=N,
        unitA=UNIT_X,
        unitB=UNIT_Y,
    )
