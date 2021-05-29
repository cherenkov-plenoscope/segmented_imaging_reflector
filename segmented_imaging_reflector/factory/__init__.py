from .. import geometry

import numpy as np
import matplotlib.pyplot as plt


def init_facet_supports_on_principal_aperture_plane(
    aperture_outer_polygon,
    aperture_inner_polygon,
    grid_spacing,
    grid_style="hexagonal"
):
    outer_radius = geometry.polygon.find_outer_radius(polygon=aperture_outer_polygon)
    N = 2*int(np.ceil(outer_radius/grid_spacing))

    if grid_style == "hexagonal":
        _grid = geometry.grid.init_hexagonal(spacing=grid_spacing, N=N)
    elif grid_style == "square":
        _grid = geometry.grid.init_square(spacing=grid_spacing, N=N)
    else:
        assert False, "Grid style {:s} is unknown.".format(grid_style)

    mask_inside_outer = geometry.polygon.mask_points_inside(
        points=_grid,
        polygon=aperture_outer_polygon
    )
    mask_inside_inner = geometry.polygon.mask_points_inside(
        points=_grid,
        polygon=aperture_inner_polygon
    )
    mask_outside_inner = np.logical_not(mask_inside_inner)

    mask_valid = np.logical_and(mask_inside_outer, mask_outside_inner)

    grid = []
    for i in range(len(_grid)):
        if mask_valid[i]:
            grid.append(_grid[i])
    grid = np.array(grid)
    return grid


# curvature / elevation


def elevate_facet_supports(
    facet_supports,
    facet_distance_optical_axis,
    facet_elevation,
):
    out = np.array(facet_supports)

    r_min = np.min(facet_distance_optical_axis)
    r_max = np.max(facet_distance_optical_axis)

    for i in range(len(out)):
        radial_distance = np.hypot(out[i, 0], out[i, 1])
        assert r_min <= radial_distance <= r_max
        elevation = np.interp(
            x=radial_distance,
            xp=facet_distance_optical_axis,
            fp=facet_elevation
        )
        out[i, 2] = elevation
    return out


def plot_points(points):
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax.set_aspect("equal")
    ax.plot(points[:, 0], points[:, 1], "xb")
    plt.show()
