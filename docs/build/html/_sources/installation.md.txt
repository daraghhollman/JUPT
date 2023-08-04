# Installation Guide

## Required Software

The JUPT code is developed and tested using Python 3.11

## Dependancies
All packages required are located in the **requirements.txt** file. These can be installed using pip, and automatically installed using the command: `pip install -r requirements.txt`

We recommend using a Python virtual enviroment.

## Installation

Navigate to your desired install directory:

`cd ~/path/to/data/directory/`

Download the repository to this location:

`git clone https://github.com/daraghhollman/JUPT`

Create a directory to store data:

`mkdir JUPT/data`

Add the path to this directory to the 'data directory' in the directory_config.ini file.

'data directory = /path/to/data/directory/data/'

### Setting up SPICE (Required for trajectories plots)
To set the tool up to work with SPICE you will need to point the 'spice directory' field in the **directory_config.ini** file to a metakernel containing data for Juno, frames, and planets.

If you don't have your own metakernel, you can create one for Juno using this tool:

* [DIASPICETools](https://github.com/mjrutala/DIASPICETools)

### Setting up Magnetospheric Boundaries
Navigate to a separate directory where you will install the [jupiter_magnetosphere_boundaries](https://github.com/DIASPlanetary/jupiter_magnetosphere_boundaries/) code. Download the github repository as follows:

`git clone https://github.com/DIASPlanetary/jupiter_magnetosphere_boundaries`

Update the **magnetosphere boundaries path** field in your directory_config.ini file under **trajectories** to point to this repository.

## Testing
To test if the tool was installed correctly, you can run the script with the default config file by running the following command from the **JUPT/** repository:
`python jupt.py default_config.ini`
