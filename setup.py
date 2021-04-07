import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="segmented_imaging_reflector",
    version="0.0",
    description="Investigating cost-effective and mass-produced segmented imaging-reflectors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sebastian Achim Mueller",
    author_email="",
    url="https://github.com/cherenkov-plenoscope/segmented_imaging_reflector",
    license="GPL v3",
    packages=["segmented_imaging_reflector"],
    python_requires=">=3",
    install_requires=["optic_object_wavefronts",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
)
