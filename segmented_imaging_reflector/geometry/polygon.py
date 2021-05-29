import numpy as np
import shapely
from shapely import geometry as shapely_geometry


def init_circle(outer_radius, num_points=1337, rotz=0.0):
    polygon = []
    for phi in np.linspace(0, 2*np.pi, num_points, endpoint=False):
        theta = phi + rotz
        point = outer_radius * np.array([np.cos(theta), np.sin(theta), 0.0])
        polygon.append(point)
    polygon = np.array(polygon)
    return polygon


def init_hexagon(outer_radius, rotz=0.0):
    return init_circle(
        outer_radius=outer_radius,
        num_points=6,
        rotz=rotz,
    )


def init_square(outer_radius, rotz=0.0):
    return init_circle(
        outer_radius=outer_radius,
        num_points=4,
        rotz=rotz,
    )


def find_outer_radius(polygon):
    max_radius = 0.0
    for point in polygon:
        radius = np.hypot(point[0], point[1])
        if radius >= max_radius:
            max_radius = radius
    return max_radius


def _to_shapely_polygon(polygon):
    poly = []
    for point in polygon:
        poly.append((point[0], point[1]))
    _line = shapely.geometry.LineString(poly)
    return shapely.geometry.Polygon(_line)


def mask_points_inside(points, polygon):
    _polygon = _to_shapely_polygon(polygon)
    mask = []
    for point in points:
        _point = shapely.geometry.Point(point[0], point[1])
        mask.append(_polygon.contains(_point))
    return np.array(mask)
