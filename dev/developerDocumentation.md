# JUPT Developer Documentation

**Contents**
* [Introduction](#Introduction)
    * [Contributing Practices](#Contributing-Practices)
* [Architecture](#Architecture)
    * [Overview](#Overview)
    * [Code Architecture](#Code-Architecture)
* [Data Sources](#Data-Sources)
    * [PDS](#PDS)
    * [AMDA](#AMDA)
    * [LESIA](#LESIA)
* [Individual Scripts](#Individual-Scripts)
    * [Common Routines](#Common-Routines)
* [Future Work](#Future-Work)


## Introduction
This is the developer documentation for JUPT. This was written to aid future developers in understanding and adding to the tool. Please note that this was written with the assumption that you have read and understand the user [documentation](https://jupt.readthedocs.io/en/latest/).

If anything is unclear, don't hesitate to contact Daragh Hollman via hollmandaragh@gmail.com, or any of the [DIAS Planetary Magnetospheres](https://www.dias.ie/cosmicphysics/astrophysics/astro-research/astro-planetary-magnetospheres/) team.

### Contributing Practices
JUPT was written in Python 3.11 and all future development should be tested in this version.

**camelCase**
* All variables should be written in **lowerCamelCase** where the first word begins with a lowercase letter and all subsequent words begin with an uppercase letter. There are some *exceptions* to this rule to help readability for instance with variants of the same variable - with the hope of making them distinct from eachother.
* All methods should be written in **UpperCamelCase**. This is similar to lowerCamelCase with the first letter capitalised.

**Release Checklist**
* Check if changes made affect the documentation in any ways. If so, update the documentation to match.
* Update `requirements.txt` to match all package requirements.
* Rebuild documentation on Read The Docs.
* Create new Zenodo version.
* Create Github release.

## Architecture

### Overview
The JUPT repo is structured in the following way:

```
JUPT
├── dev
│   └── developerDocumentation.md
├── docs
│   ├── build
│   │   ├── doctrees
│   │   └── html
│   ├── make.bat
│   ├── Makefile
│   └── source
│       ├── advancedConfig.md
│       ├── basicConfig.md
│       ├── conf.py
│       ├── contributingGuidelines.md
│       ├── futureWork.md
│       ├── index.rst
│       ├── installation.md
│       ├── intro.md
│       ├── rulesOfUse.md
│       └── usage.md
├── JUPT
│   ├── input_config
│   │   └──input_files.ini
│   ├── JUPT_output
│   │   └── default_config.png
│   ├── default_config.ini
│   ├── directory_config.ini
│   ├── junoDerivedMoments.py
│   ├── junoEphemeris.py
│   ├── junoJADE_ions.py
│   ├── junoJade.py
│   ├── junoMAG.py
│   ├── junoTrajectories.py
│   ├── junoWAVES.py
│   ├── jupt.py
│   ├── pdsBinaryTools.py
│   ├── userAdditions.py
│   └── vLines.py
├── LICENSE
├── README.md
└── requirements.txt
```

**dev**

`dev` is a folder for developer specific information. Files should be placed here if the general user is unexpected to need them, but a (future) developer will.

**docs**

`docs` contains the documentation for the readTheDocs page. These are markdown files written under `docs/source/` which are compiled using **sphinx** from the `docs` directory.

The following command should be used to build the documentation successfully:

```shell
make clean; make html
```

**JUPT**

The `JUPT` directory contains the program scripts including all config files and all outputs.

### Code Architecture
`jupt.py` is the main file of the tool. It is run in the following way:

```shell
python jupt.py path/to/config.ini
```

This file imports all other scripts in the tool and reads the config file to decide which to call from. It creates the matplotlib subplots which it passes to each script to be plotted.

Each of those scripts handles the retrieval, loading, processing, and plotting of its respective data.

## Data Sources

### PDS
The Planetary Data System can be found at this [link](https://pds.nasa.gov/), more specifically, we retrieve our PDS data from [Planetary Plasma Interactions](https://pds-ppi.igpp.ucla.edu/) node.

### AMDA
The AMDA database can be accessed via this [link](http://amda.irap.omp.eu/).

In the code, AMDA should be interacted with through the package [speasy](https://speasy.readthedocs.io/en/latest/).

### LESIA

The tool uses the Juno/Waves estimated flux density Collection (Version 01) by Louis et al. DOI https://doi.org/10.25935/6jg4-mk86

## Individual Scripts

`junoMAG.py`
* Downloads from: AMDA
* Plots: Time series
* Options including choice of coordinate system, comparison with a lobe field model

`junoWAVES.py`
* Downloads from: LESIA
* Plots: Colourmap
* Handles Waves for a selected frequency range

`junoJade.py`
* Downloads from: PDS
* Plots: Colourmap
* Handles JADE electrons energies and pitch angles

`junoJADE_ions`
* Downloads from: PDS
* Plots: Colourmap
* Handles JADE ions summed over a range of time of flights

`junoEphemeris`
* Downloads from: AMDA
* Plots: Axis formatting and tick labels

`junoTrajectories`
* Loads from: SPICE metakernel
* Plots: Trajectory diagrams in xy, xz, yz

`junoDerivedMoments`
* Unfinished and nonfunctional

`pdsBinaryTools.py`
* Handles loading data from linked binary (.DAT) and label (.LBL) files.

`userAdditions`
* A file which is passed the figure and all axes from the plot, for the user to make any changes external to the code.

`vLines.py`
* Handles the adding of vertical lines across the plots, be it manual or automatically from a loaded file.

### Common Routines

`PathFromTimeDifference` is a function in `junoWAVES.py` which creates output path names for each day between two times in a specified format. This is called from any file which downloads data automatically from PDS or LESIA.

`pdsBinaryTools.py` contains functions for downloadind and reading binary data from the PDS. It uses the label files downloaded to understand how to read the binary files.

## Future Work

Two features are most important to impliment next. These are [JADE](https://pds-ppi.igpp.ucla.edu/search/view/?f=yes&id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0) ions for specific ions, not just a range of TOF, and also [JEDI](https://pds-ppi.igpp.ucla.edu/search/view/?f=yes&id=pds://PPI/JNO-J-JED-3-CDR-V1.0) data.
