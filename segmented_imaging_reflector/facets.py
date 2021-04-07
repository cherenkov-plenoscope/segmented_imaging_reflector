import numpy as np
import optic_object_wavefronts as oow

UNIT_HEX_Y_A = np.array([0.0, 1.0, 0.0])
UNIT_HEX_Y_B = np.array([np.sqrt(3) / 2, 0.5, 0.0])


def make_facet_supports(
    facet_outer_radius,
    gap_between_facets,
    max_outer_aperture_radius,
    min_inner_aperture_radius,
    facet_z_poly3,
):
    facet_bound_outer_radius = facet_outer_radius + 0.5 * gap_between_facets
    facet_spacing = facet_bound_outer_radius * np.sqrt(3.0)

    # grid with too much supports
    N = 2 * int(np.ceil(max_outer_aperture_radius / facet_spacing))
    all_facet_supports = {}
    for dA in np.arange(-N, N + 1, 1):
        for dB in np.arange(-N, N + 1, 1):
            all_facet_supports[(dA, dB)] = facet_spacing * (
                dA * UNIT_HEX_Y_B + dB * UNIT_HEX_Y_A
            )

    # is indside inner/outer radii
    facet_supports = {}
    for fkey in all_facet_supports:
        facet_support_radius = np.hypot(
            all_facet_supports[fkey][0], all_facet_supports[fkey][1]
        )
        outer_mirror_edge_radius = facet_support_radius + facet_outer_radius
        inner_mirror_edge_radius = facet_support_radius - facet_outer_radius

        if outer_mirror_edge_radius <= max_outer_aperture_radius:
            if inner_mirror_edge_radius >= min_inner_aperture_radius:
                facet_supports[fkey] = all_facet_supports[fkey]

    # elevate facets
    for fkey in facet_supports:
        facet_support_radius = np.hypot(
            facet_supports[fkey][0], facet_supports[fkey][1]
        )
        support_z = np.polyval(p=facet_z_poly3, x=facet_support_radius)
        facet_supports[fkey][2] = support_z

    return facet_supports


def make_facet_rotation(
    facet_support, alignment_point,
):
    facet_support_xy = [facet_support[0], facet_support[1], 0]
    facet_support_radius = np.linalg.norm(facet_support_xy)

    if facet_support_radius > 0:
        principal_optical_axis = np.array([0, 0, 1])

        facet_normal = alignment_point - facet_support
        distance_to_alignment_point = np.linalg.norm(facet_normal)
        assert distance_to_alignment_point > 0.0
        facet_normal = facet_normal / distance_to_alignment_point

        facet_support_xy = facet_support_xy / facet_support_radius
        rot_axis = np.cross(facet_normal, facet_support_xy)

        angle_between_optical_axis_and_normal = np.arccos(
            np.dot(principal_optical_axis, facet_normal)
        )

        rot = {
            "repr": "axis_angle",
            "axis": rot_axis.tolist(),
            "angle_deg": float(
                -1.0 * np.rad2deg(angle_between_optical_axis_and_normal)
            ),
        }
    else:
        rot = {"repr": "tait_bryan", "xyz_deg": [0, 0, 0]}

    return rot


def make_facet_alignment_points(
    facet_supports, alignment_point_z_poly3,
):
    alignment_points = {}
    for fkey in facet_supports:
        facet_support_radius = np.hypot(
            facet_supports[fkey][0], facet_supports[fkey][1]
        )
        alignment_z = np.polyval(
            p=alignment_point_z_poly3, x=facet_support_radius
        )
        alignment_points[fkey] = [0, 0, alignment_z]
    return alignment_points


def make_facet_rotations(facet_supports, facet_alignment_points):
    facet_rotations = {}
    for fkey in facet_supports:
        facet_rotations[fkey] = make_facet_rotation(
            facet_support=facet_supports[fkey],
            alignment_point=facet_alignment_points[fkey],
        )
    return facet_rotations


def make_facet_ids(facet_supports, facet_id_start):
    facet_ids = {}
    facet_id = int(facet_id_start)
    for fkey in facet_supports:
        facet_ids[fkey] = int(facet_id)
        facet_id += 1
    return facet_ids
