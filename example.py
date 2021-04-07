import segmented_imaging_reflector as sir

job = sir.init_job(job=sir.example_job)
scn = sir.make_scenery(job=job)
sir.merlict_c89.write_scenery(scenery=scn, path="segmented_mirror.tar")
