# Juno Universal Plotting Tool
*An all in one tool for creating plots using data from the Juno spacecraft*

JUPT - The **J**uno **U**niversal **P**lotting **T**ool - is an all in one tool for creating and customising plots of any combination of data from the Juno spacecraft, inlcuding (but not limited to) MAG, Waves, and Trajectories.

![sampleFigure](https://github.com/daraghhollman/JUPT/assets/62439417/9f8834ee-ef1b-4198-a058-f9f649da1a18)

This project is currently a work in progress with updates being posted here frequently. The project is **currently not in a functional state**.

## Instructions

### Config
Edit the configuration settings in **config.ini**:

#### data
|key|description|
|----|----|
|data directory|A path pointing to the directory where the data will we automatically downloaded and stored. e.g. /home/user/data/|

#### plotting
|key|description|
|---|---|
|start time|The time with which to start your plot from. Must be in the format YYYY-MM-DDTHH:MM:SS|
|end time|The time with which to end your plot. Must be in the format YYYY-MM-DDTHH:MM:SS|
|plot Waves|Should Waves data be plotted. Must be either **True** or **False**|
|plot MAG|Should MAG data be plotted. Must be either **True** or **False**|
|panel spacing|The white space vertically between panels in units of panel height. (**default: 0**)|
|~~font size~~|Base fontsize for the plot. Currently not functional due to **issue #9** (**default: 11**)|
|major tick length|Length of major ticks. (**defaultL: 12**)|
|minor tick length|Length of minor ticks. (**default: 8**)|
|major tick width|Width of major ticks. (**default: 0.8**)|
|minor tick width|Width of minor ticks. (**default: 0.8**)|

#### Waves
|key|description|
|---|---|
|frequency limit|The range of frequency bins in kHz to display on the plot. (**default: [0.2, 139]**)|
|colour map|The matplotlib colour map for the Waves data. Some example colourblind friendly (and perpetually uniform) options are: viridis, plasma, inferno, and magma. (**default: viridis**)|

#### MAG
|key|description|
|---|---|
|plot magnitude|Should the magnetic field magnitude be plotted. Must be either **True** or **False**.|
|plot cartesians|Should the magnetic field cartesian components be plotted. Must be either **True** or **False**.|
|plot polars|Should the magnetic field polar components be plotted. Must be either **True** or **False**.|
|plot lobe|Should the lobe field magnitude be plotted. Must be either **True** or **False**.|
|plot lobe uncertainty|Should the lobe field uncertainty be plotted. Must be either **True** or **False**.|
|line width|Line width (matplotlib) of the MAG data. (**default: 0.5**)|

Note that the lobe field plotted is the Khurana model.

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

### Running

Run `python jupt.py` to create the plot.

Note, the figure is not automatically saved.
