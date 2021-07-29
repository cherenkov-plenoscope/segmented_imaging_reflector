/*
estimate the light-field-geometry of segemted imaging reflectors
*/

#include "../merlict_c89/merlict_c89/all_headers.h"
#include "../merlict_c89/merlict_c89/all_sources.c"

struct mliPhoton draw_photon(
        struct mliPrng *prng,
        double aperture_radius_m,
        double opening_angle_deg,
        double distance_to_aperture_plane) {

        struct mliRandomUniformRange azimuth_range;
        struct mliRandomZenithRange zenith_range;

        struct mliVec incident_direction;
        struct mliVec creation_position;
        struct mliVec support_position;

        struct mliPhoton photon;

        azimuth_range.start = 0.0;
        azimuth_range.range = 2.0 * MLI_PI;

        zenith_range = mliRandomZenithRange_set(
                0.0,
                mli_deg2rad(opening_angle_deg));

        support_position = mli_random_position_on_disc(
                aperture_radius_m,
                prng);

        /*
        fprintf(stderr, "support_position (%f,%f,%f)\n", support_position.x, support_position.y, support_position.z);
        */
        incident_direction = mli_random_draw_direction_in_zenith_azimuth_range(
                zenith_range,
                azimuth_range,
                prng);

        /*
        fprintf(stderr, "incident_direction (%f,%f,%f)\n", incident_direction.x, incident_direction.y, incident_direction.z);
        */

        creation_position = mliVec_add(
                support_position,
                mliVec_multiply(
                        incident_direction,
                        distance_to_aperture_plane)
        );

        /*
        fprintf(stderr, "creation_position (%f,%f,%f)\n", creation_position.x, creation_position.y, creation_position.z);
        */
        photon.ray.support = creation_position;
        photon.ray.direction = mliVec_multiply(incident_direction, -1.0);
        photon.wavelength = 433e-9;

        return photon;
}


int main(int argc, char *argv[])
{
        uint64_t seed = 0;
        struct mliPrng prng = mliPrng_init_MT19937(seed);
        struct mliScenery scenery = mliScenery_init();
        double aperture_radius_m = 0.0;
        double opening_angle_deg = 0.0;
        const double DISTANCE_TO_APERTURE_PLANE = 1e2;
        const uint64_t MAX_ITERATIONS = 16;
        const uint64_t SENSOR_ID = 0;
        uint64_t num_hits = 0;
        uint64_t num_photons = 0;
        uint64_t i;

        mli_check(
                argc == 6,
                "Expected 3 arguments.\n"
                "1) scenery-path\n"
                "2) aperture_radius_m\n"
                "3) opening_angle_deg\n"
                "4) num_photons\n"
                "5) seed");

        mli_check(
                mli_string_ends_with(argv[1], ".tar"),
                "Expected arcv[1] to end with '.tar'");
        mli_check(
                mliScenery_malloc_from_tar(&scenery, argv[1]),
                "Can not read scenery from '.tar'.");

        mli_check(
                mli_string_to_float(&aperture_radius_m, argv[2]),
                "Can not parse aperture_radius_m from argv[2].");
        mli_check(
                aperture_radius_m > 0.0,
                "Expected aperture_radius_m > 0.0.");

        mli_check(
                mli_string_to_float(&opening_angle_deg, argv[3]),
                "Can not parse opening_angle_deg from argv[3].");
        mli_check(
                opening_angle_deg > 0.0,
                "Expected opening_angle_deg > 0.0.");

        mli_check(
                mli_string_to_uint(&num_photons, argv[4], 10),
                "Can not parse num_photons from argv[4].");

        mli_check(
                mli_string_to_uint(&seed, argv[5], 10),
                "Can not parse num_photons from argv[5].");

        prng = mliPrng_init_MT19937(seed);

        for (i = 0; i < num_photons; i++) {
                int hit = 0;
                uint64_t idx_final_interaction = 0;
                struct mliPhotonInteraction final_interaction;
                struct mliPhoton photon = draw_photon(
                        &prng,
                        aperture_radius_m,
                        opening_angle_deg,
                        DISTANCE_TO_APERTURE_PLANE);

                struct mliDynPhotonInteraction history = mliDynPhotonInteraction_init();
                mli_c(mliDynPhotonInteraction_malloc(&history, MAX_ITERATIONS));

                mli_check(
                        mli_propagate_photon(
                                &scenery,
                                &history,
                                &photon,
                                &prng,
                                MAX_ITERATIONS),
                        "Failed to propagate."
                );

                idx_final_interaction = history.size - 1;
                final_interaction = history.array[idx_final_interaction];

                if (final_interaction.on_geometry_surface) {
                        uint64_t robj = final_interaction.geometry_id.robj;
                        uint64_t id = scenery.geometry.robjects[robj];
                        if (id == SENSOR_ID) {
                                hit = 1;

                        }
                }


                if (hit) {
                        num_hits += 1;
                        /*
                        fprintf(
                                stdout,
                                "%e,%e\n",
                                final_interaction.position_local.x,
                                final_interaction.position_local.y);
                        */
                } else {
                        /*
                        fprintf(stdout, "-\n");
                        */
                }

                mliDynPhotonInteraction_free(&history);
        }

        fprintf(stderr, "eff. %.3f\n", (double)num_hits/(double)num_photons);


        mliScenery_free(&scenery);
        return EXIT_SUCCESS;
error:
        return EXIT_FAILURE;
}
