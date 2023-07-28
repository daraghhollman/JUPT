# Juno Universal Plotting Tool
*An all in one tool for creating plots using data from the Juno spacecraft*

JUPT - The **J**uno **U**niversal **P**lotting **T**ool - is an all in one tool for creating and customising plots of any combination of data from the Juno spacecraft, inlcuding (but not limited to) MAG, Waves, JADE and Trajectories.

![sampleFigure](https://github.com/daraghhollman/JUPT/assets/62439417/9f8834ee-ef1b-4198-a058-f9f649da1a18)

This project is currently a work in progress with updates being posted here frequently. The project is **currently not in a functional state**.

## Instructions

### Installation
Navigate to your desired install directory:

`cd ~/path/to/data/directory/`

Download the repository to this location:

`git clone https://github.com/daraghhollman/JUPT`

Create a directory to store data:

`mkdir ./data`

Add the path to this directory to the 'data directory' in the config.ini file.

#### Setting up SPICE (Required for trajectories plots)
Navigate to your desired directory. (This will contain all of your spice kernels which will be a large number of files.)

`cd ~/path/to/spice/directory/`

Download the DIASPICETools repository:

`git clone https://github.com/mjrutala/DIASPICETools`

Open this directory, and run the tool using a python terminal:

`cd DIASPICETools/`

`python` (the command to open a python terminal may be different on your system)

*In the python terminal:*
`from make_Metakernel import *`
`make_Metakernel("Juno", "/full/path/to/spice/directory")`

This will download the required SPICE kernels to `.../DIASPICETools/SPICE/`. This may take some time.

Simply exit the python terminal and edit the 'spice directory' in config.ini file with the path to this `.../SPICE/` directory.


### Config
Edit the configuration settings in **config.ini** as explained in section "config.ini"

### Running

Run `python jupt.py` to create the plot.

Note, the figure is not automatically saved.


## config.ini
#### data
|key|description|
|----|----|
|data directory|A path pointing to the directory where the data will we automatically downloaded and stored. e.g. /home/user/data/|
|download new data|Should new data be downloaded regardless. If False, missing data will still be automatically downloaded. Must be either **True** or **False**.|

#### plotting
|key|description|
|---|---|
|start time|The time with which to start your plot from. Must be in the format YYYY-MM-DDTHH:MM:SS|
|end time|The time with which to end your plot. Must be in the format YYYY-MM-DDTHH:MM:SS|
|plot Waves|At what subplot index should Waves data be plotted. Leave as 0 to not plot Waves|
|plot JADE electron energies|At what subplot index should JADE electron energies data be plotted. Leave as 0 to not plot|
|plot JADE electron pitch angles|At what subplot index should JADE electron pitch angles data be plotted. Leave as 0 to not plot|
|plot MAG|At what subplot index should MAG data be plotted. Leave as 0 to not plot MAG|
|panel spacing|The white space vertically between panels in units of panel height. Note, this can be 0. (**default: 0.1**)|
|~~font size~~|Base fontsize for the plot. Currently not functional due to **issue #9** (**default: 11**)|
|major tick length|Length of major ticks. (**default: 16**)|
|minor tick length|Length of minor ticks. (**default: 8**)|
|major tick width|Width of major ticks. (**default: 0.8**)|
|minor tick width|Width of minor ticks. (**default: 0.8**)|
|y tick length|Length of major ticks on the y axes. (**default: 12**)|
|y tick width|Width of major ticks on the y axes. (**default: 0.8**)|

#### colours
|key|description|
|---|---|
|magnitude colour|The colour (matplotlib) of the magnitude of the MAG data. (**default: black**)|
|component colours|The colours (matplotlib) of the coordinate components of the MAG data. Must be formated as ["colour1", "colour2", "colour3"]. (**default: ["indianred","mediumturquoise","cornflowerblue"]**)|
|lobe colour|The colour (matplotlib) of the lobe field and its uncertainty. (**default: gold**)|

#### vertical lines
|key|description|
|---|---|
|read from file|Should boundary crossings be read from file|
|file path|The path to the file to read boundary crossings from. Should be a csv file in the format of a pandas dataframe.|
|file line colour|Colour of boundary crossing vertical lines. (**default: red**)|
|labels|Labels for manually placed vertical lines. In the format of ["Label1","label2",...["labelN"]]|
|positions|Positions of manually placed vertical lines. In the format of ["position1", "position2",... "positionN"], where each position follows the format YYYY-MM-DDTHH:MM:SS. Leave as [] for no vertical lines|
|colours|Colours for each manually placed line to allow for different colours for each line. Must be in the format ["colour1", "colour2",... "colourN"]|
|linestyle|The matplotlib linestyle of the vertical lines. (**default: --** i.e. dashed)|

#### Waves
|key|description|
|---|---|
|frequency limit|The range of frequency bins in kHz to display on the plot. (**default: [1, 149]**)|
|colour map|The matplotlib colour map for the Waves data. Some example colourblind friendly (and perpetually uniform) options are: viridis, plasma, inferno, and magma. (**default: viridis**)|
|frequency bins|The new number of frequency bins to interpolate the data to. Leave as 126 for no interpolation (**default: 200**).|
|y scale|y axis scaling options for the Waves plot. i.e. linear, log. (**default: log**)|

#### JADE
|key|description|
|---|---|
|pitch angle energy range|Range of energies (in eV) to average across to calculate the pitch angle data. Leave as [] to average across all energies.|
|bin pitch angles|Should the pitch angle data be binned into regular chunks of degrees. (**default: True**)|
|bin size|The size, in degrees, of these bins. (**default: 10**)|
|colour map|The matplotlib colormap for JADE data. (**default: magma**)|
|high resolution|The JADE instrument splits its data into two modes, a high resolution (sampling every second) and a low resolution (integrating over 30s, approx. one full spacecraft rotation). Note: For times containing high resolution data there is an absence of low resolution data. (**default: True**)|

#### MAG
|key|description|
|---|---|
|plot magnitude|Should the magnetic field magnitude be plotted. Must be either **True** or **False**.|
|plot cartesians|Should the magnetic field cartesian components be plotted. Must be either **True** or **False**.|
|plot polars|Should the magnetic field polar components be plotted. Must be either **True** or **False**.|
|plot lobe|Should the lobe field magnitude be plotted (Khurana model: K & K 2002). Must be either **True** or **False**.|
|plot lobe uncertainty|Should the lobe field uncertainty be plotted. Must be either **True** or **False**.|
|line width|Line width (matplotlib) of the MAG data. (**default: 0.5**)|



