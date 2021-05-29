import segmented_imaging_reflector as sir

job = dict(sir.example_job)

reflgeom = sir.init_reflector_geometry(config=job["reflector"])
scn = sir.make_test_bench_scenery(job=job, reflector_geometry=reflgeom)
sir.merlict_c89.write_scenery(scenery=scn, path="segmented_mirror.tar")
