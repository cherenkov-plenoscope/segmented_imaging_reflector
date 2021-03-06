import numpy as np
import optic_object_wavefronts as oow


FACET_ID_START = 1000000
IMAGE_SENSOR_ID = 0


def add_image_sensor_to_scenery(scenery, image_sensor_config):
    isc = image_sensor_config

    _image_sensor_mesh = oow.primitives.spherical_cap_pixels.init(
        outer_radius=isc["radius_m"],
        curvature_radius=isc["curvature_radius_m"],
        n_hex_grid=isc["num_pixel_on_diagonal"],
    )
    scenery["objects"]["image_sensor"] = oow.Wavefront.init_from_Object(
        obj=_image_sensor_mesh
    )
    image_sensor_ref = {
        "id": IMAGE_SENSOR_ID,
        "pos": [
            0,
            0,
            isc["distance_to_principal_aperture_plane_m"],
        ],
        "rot": {"repr": "tait_bryan", "xyz_deg": [0, 0, 0]},
        "obj": "image_sensor",
        "mtl": {"SphericalPixelCap": "screen"},
    }
    scenery["tree"]["children"].append(image_sensor_ref)

    _housing_radius = isc["additional_housing_radius_m"] + isc["radius_m"]
    _screen_shield_mesh = oow.primitives.disc.init(
        outer_radius=_housing_radius, n=isc["polygon_density"] * 3,
    )
    scenery["objects"]["image_sensor_shield"] = oow.Wavefront.init_from_Object(
        obj=_screen_shield_mesh
    )
    _curvature_gap = 0.05
    image_sensor_shield_ref = {
        "id": IMAGE_SENSOR_ID + 1,
        "pos": [
            0,
            0,
            isc["distance_to_principal_aperture_plane_m"]
            + _curvature_gap,
        ],
        "rot": {"repr": "tait_bryan", "xyz_deg": [0, 0, 0]},
        "obj": "image_sensor_shield",
        "mtl": {"disc": "screen_shield"},
    }
    scenery["tree"]["children"].append(image_sensor_shield_ref)

    return scenery


def add_facets_to_scenery(scenery, reflector_config, reflector_geometry):
    MIRROR_FACET_OBJECT_KEY = "mirror_facet"
    rg = reflector_geometry
    rc = reflector_config

    _facet_mesh = oow.primitives.spherical_planar_lens_hexagonal.init(
        outer_radius=rc["facet"]["outer_radius_m"],
        curvature_radius=rc["facet"]["curvature_radius_m"],
        width=rc["facet"]["width_m"],
        n=rc["polygon_density"],
    )
    scenery["objects"][MIRROR_FACET_OBJECT_KEY] = oow.Wavefront.init_from_Object(
        obj=_facet_mesh
    )

    MIRROR_FACET_MATERIAL_KEYS = {
        "SphericalPlaneHexagonalBody_front": "mirror_surface",
        "SphericalPlaneHexagonalBody_back": "mirror_back",
        "SphericalPlaneHexagonalBody_side": "mirror_back",
    }

    for fkey in rg["facet_supports"]:
        facet_ref = {
            "id": int(rg["facet_ids"][fkey]),
            "pos": list(rg["facet_supports"][fkey]),
            "rot": dict(rg["facet_rotations"][fkey]),
            "obj": str(MIRROR_FACET_OBJECT_KEY),
            "mtl": dict(MIRROR_FACET_MATERIAL_KEYS),
        }
        scenery["tree"]["children"].append(facet_ref)

    return scenery


def init_scenery():
    functions = {
        "positiv_infinity": [[200e-9, 9e99], [1200e-9, 9e99],],
        "unity": [[200e-9, 1.0], [1200e-9, 1.0],],
        "zero": [[200e-9, 0.0], [1200e-9, 0.0],],
        "mirror_reflectivity": [[200e-9, 1.0], [1200e-9, 1.0],],
    }

    materials = {
        "colors": [
            {"rgb": [122, 91, 49], "name": "brown"},
            {"rgb": [22, 91, 149], "name": "blue"},
            {"rgb": [200, 200, 200], "name": "grey"},
            {"rgb": [200, 0, 0], "name": "red"},
        ],
        "media": [
            {
                "name": "vacuum",
                "refraction": "unity",
                "absorbtion": "positiv_infinity",
            },
        ],
        "default_medium": "vacuum",
        "surfaces": [
            {
                "name": "mirror_surface",
                "material": "Phong",
                "specular_reflection": "mirror_reflectivity",
                "diffuse_reflection": "zero",
                "color": "grey",
            },
            {
                "name": "mirror_back",
                "material": "Phong",
                "specular_reflection": "zero",
                "diffuse_reflection": "zero",
                "color": "brown",
            },
            {
                "name": "screen",
                "material": "Phong",
                "specular_reflection": "zero",
                "diffuse_reflection": "zero",
                "color": "blue",
            },
        ],
        "boundary_layers": [
            {
                "name": "mirror_surface",
                "inner": {"medium": "vacuum", "surface": "mirror_surface"},
                "outer": {"medium": "vacuum", "surface": "mirror_surface"},
            },
            {
                "name": "mirror_back",
                "inner": {"medium": "vacuum", "surface": "mirror_back"},
                "outer": {"medium": "vacuum", "surface": "mirror_back"},
            },
            {
                "name": "screen",
                "inner": {"medium": "vacuum", "surface": "screen"},
                "outer": {"medium": "vacuum", "surface": "screen"},
            },
            {
                "name": "screen_shield",
                "inner": {"medium": "vacuum", "surface": "mirror_back"},
                "outer": {"medium": "vacuum", "surface": "mirror_back"},
            },
        ],
    }

    scenery = {
        "tree": {"children": []},
        "objects": {},
        "functions": functions,
        "materials": materials,
    }
    return scenery
