from . import merlict_c89
from . import facets
from . import scenery

example_job = {
    "polygon_density": 17,
    "image_sensor": {
        "num_pixel_on_diagonal": 64,
        "radius_m": 0.35,
        "additional_housing_radius_m": 0.05,
        "curvature_radius_m": 100.0,
        "distance_to_principal_aperture_plane_m": 5.0,
    },
    "reflector": {
        "max_outer_radius_m": 1.8,
        "min_inner_radius_m": 0.1,
        "facet": {
            "shape": "hexagonal",
            "outer_radius_m": 0.305,
            "gap_between_m": 0.01,
            "curvature_radius_m": 40.0,
            "width_m": 0.025,
            "alignment_point_z_poly3_m": [0.0, 0.0, 0.0, 10.0],
        },
        "z_poly3_m": [0.01, 0.05, 0.0, 0.0],
    },
}


def init_job(job):
    job["reflector"]["facet_supports"] = facets.make_facet_supports(
        facet_outer_radius=job["reflector"]["facet"]["outer_radius_m"],
        gap_between_facets=job["reflector"]["facet"]["gap_between_m"],
        max_outer_aperture_radius=job["reflector"]["max_outer_radius_m"],
        min_inner_aperture_radius=job["reflector"]["min_inner_radius_m"],
        facet_z_poly3=job["reflector"]["z_poly3_m"],
    )
    job["reflector"]["facet_alignment_points"] = facets.make_facet_alignment_points(
        facet_supports=job["reflector"]["facet_supports"],
        alignment_point_z_poly3=job["reflector"]["facet"][
            "alignment_point_z_poly3_m"
        ],
    )
    job["reflector"]["facet_rotations"] = facets.make_facet_rotations(
        facet_supports=job["reflector"]["facet_supports"],
        facet_alignment_points=job["reflector"]["facet_alignment_points"],
    )
    job["reflector"]["facet_ids"] = facets.make_facet_ids(
        facet_supports=job["reflector"]["facet_supports"],
        facet_id_start=scenery.FACET_ID_START,
    )
    return job


def make_scenery(job):
    scn = scenery.init_scenery()
    scn = scenery.add_image_sensor_to_scenery(scenery=scn, job=job)
    scn = scenery.add_facets_to_scenery(scenery=scn, job=job)
    return scn
