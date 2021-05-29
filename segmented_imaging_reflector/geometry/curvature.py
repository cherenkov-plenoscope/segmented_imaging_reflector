import numpy as np


def parabolic(radius, focal_length):
    return 1.0 / (4.0 * focal_length) * radius ** 2.0


def spherical(radius, curvature_radius):
    return curvature_radius - np.sqrt(curvature_radius ** 2 - radius ** 2)
