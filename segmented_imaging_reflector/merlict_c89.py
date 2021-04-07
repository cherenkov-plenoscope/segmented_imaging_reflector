import numpy as np
import tarfile
import io
import json
import optic_object_wavefronts as oow


def write_scenery(scenery, path):
    with tarfile.open(path, mode="w") as tarout:

        # functions
        for fun_key in scenery["functions"]:
            function_array = np.array(scenery["functions"][fun_key])
            function_csv_str = _array_to_csv_str(function_array)
            _tar_append(
                tarout=tarout,
                file_name="functions/{:s}.csv".format(fun_key),
                file_bytes=str.encode(function_csv_str),
            )

        # objects
        for obj_key in scenery["objects"]:
            object_wavefront_str = oow._obj_to_wavefront(
                obj=scenery["objects"][obj_key]
            )
            _tar_append(
                tarout=tarout,
                file_name="objects/{:s}.obj".format(obj_key),
                file_bytes=str.encode(object_wavefront_str),
            )

        # materials
        materials_json_str = json.dumps(scenery["materials"], indent=2)
        _tar_append(
            tarout=tarout,
            file_name="materials.json",
            file_bytes=str.encode(materials_json_str),
        )

        # tree
        tree_json_str = json.dumps(scenery["tree"], indent=0)
        _tar_append(
            tarout=tarout,
            file_name="tree.json",
            file_bytes=str.encode(tree_json_str),
        )


def _array_to_csv_str(x):
    x_csv_str = []
    for _p in x:
        x_csv_str.append("{:e},{:e}\n".format(_p[0], _p[1]))
    return "".join(x_csv_str)


def _tar_append(tarout, file_name, file_bytes):
    with io.BytesIO() as buff:
        info = tarfile.TarInfo(file_name)
        info.size = buff.write(file_bytes)
        buff.seek(0)
        tarout.addfile(info, buff)
