# Advanced Configuration

More detailed configuration options for those who wish to customise their plots further. This includes both style options, but also more complex plotting settings which require a scientific understanding.

These plotting options correspond to the *dynamic* config file, as described in the [Basic Configuration](basicConfig) section.

For each section, reference in the config file should look as in the following example:
```
[section]
key = 
```

## plotting
|key|description|
|---|---|
|start time|The time with which to start your plot from. Must be in the format YYYY-MM-DDTHH:MM:SS|
|end time|The time with which to end your plot. Must be in the format YYYY-MM-DDTHH:MM:SS|
|plot trajectories|At what subplot index should trajectories data be plotted. Leave as 0 to not plot trajectories.|
|plot Waves|At what subplot index should Waves data be plotted. Leave as 0 to not plot Waves|
|plot JADE electron energies|At what subplot index should JADE electron energies data be plotted. Leave as 0 to not plot|
|plot JADE electron pitch angles|At what subplot index should JADE electron pitch angles data be plotted. Leave as 0 to not plot|
|plot MAG|At what subplot index should MAG data be plotted. Leave as 0 to not plot MAG|
|panel spacing|The white space vertically between panels in units of panel height. Note, this can be 0. (**default: 0.2**)|
|~~font size~~|Base fontsize for the plot. Currently not functional due to **issue #9** (**default: 11**)|
|major tick length|Length of major ticks. (**default: 16**)|
|minor tick length|Length of minor ticks. (**default: 8**)|
|major tick width|Width of major ticks. (**default: 0.8**)|
|minor tick width|Width of minor ticks. (**default: 0.8**)|
|y tick length|Length of major ticks on the y axes. (**default: 12**)|
|y tick width|Width of major ticks on the y axes. (**default: 0.8**)|

## Waves
|key|description|
|---|---|
|frequency limit|The range of frequency bins in kHz to display on the plot. (**default: [1, 149]**)|
|colour map|The matplotlib colour map for the Waves data. Some example colourblind friendly (and perpetually uniform) options are: viridis, plasma, inferno, and magma. (**default: viridis**)|
|frequency bins|The new number of frequency bins to interpolate the data to. Leave as 126 for no interpolation (**default: 200**).|
|y scale|y axis scaling options for the Waves plot. i.e. linear, log. (**default: log**)|

## JADE
|key|description|
|---|---|
|pitch angle energy range|Range of energies (in eV) to average across to calculate the pitch angle data. Leave as [] to average across all energies.|
|bin pitch angles|Should the pitch angle data be binned into regular chunks of degrees. (**default: True**)|
|bin size|The size, in degrees, of these bins. (**default: 10**)|
|colour map|The matplotlib colormap for JADE data. (**default: magma**)|
|high resolution|The JADE instrument splits its data into two modes, a high resolution (sampling every second) and a low resolution (integrating over 30s, approx. one full spacecraft rotation). Note: For times containing high resolution data there is an absence of low resolution data. Note, this tool can mis-create plots which contain sections of time containing both resolutions. These mis-creations can be easily noticed by a discontinuity in tick labels. (**default: False**)|

## JADE Ions
|key|description|
|---|---|
|colour map|The matplotlib colormap for JADE Ion data. (**default: plasma**)|
|TOF range|What time of flight values (seconds) to sum. Leave as [] to sum over all time of flight values.|

## MAG
|key|description|
|---|---|
|plot magnitude|Should the magnetic field magnitude be plotted. Must be either **True** or **False**.|
|plot cartesians|Should the magnetic field cartesian components be plotted. Must be either **True** or **False**.|
|plot polars|Should the magnetic field polar components be plotted. Must be either **True** or **False**.|
|plot lobe|Should the lobe field magnitude be plotted (Khurana model: K & K 2002). Must be either **True** or **False**.|
|plot lobe uncertainty|Should the lobe field uncertainty be plotted. Must be either **True** or **False**.|
|line width|Line width (matplotlib) of the MAG data. (**default: 0.5**)|
|magnitude colour|The colour (matplotlib) of the magnitude of the MAG data. (**default: black**)|
|component colours|The colours (matplotlib) of the coordinate components of the MAG data. Must be formated as ["colour1", "colour2", "colour3"]. (**default: ["indianred","mediumturquoise","cornflowerblue"]**)|
|lobe colour|The colour (matplotlib) of the lobe field and its uncertainty. (**default: gold**)|

## Trajectories
|key|description|
|---|---|
|BS dynamic pressure|Dynamic pressure (nPa) to be passed to the Joy model bow shock. Joy et al. (2002)|
|MP dynamic pressure|Dynamic pressure (nPa) to be passed to the Joy model magetopause. Joy et al. (2002)|
|plot bow shock|Should the Joy model bow shock be plotted on the trajectories plots|
|plot magnetopause|Should the Joy model magnetopause be plotted on the trajectories plots|
|bow shock colour|What colour should the bow shock model be on the plot.|
|magnetopause colour|What colour should the magnetopause model be on the plot.|
|frame|What SPICE frame should the trajectories be plotted in. Common options include JUNO_JSS and JUNO_JSO. Note that magnetospheric boundaries can only currently be plotted using JSS.|
|plotted colour|Matplotlib colour to denote the section of orbit being plotted in the panels.|
|extension colour|Matplotlib colour to denote the orbit before and after the section of orbit being plotted in the panels.|
|time extensions|How long before and after the data plotted should the trajectory plot be extended. (In units of days)|
|major tick length|Major tick length for the trajectories plots|
|minor tick length|Minor tick length for the trajectories plots|
|major tick multiple|Major ticks will be placed at a multiple of this number.|
|minor tick multiple|Minor ticks will be placed at a multiple of this number.|
|x bounds|The bounds of the x axis on the trajectory plots|
|y bounds|The bounds of the y axis on the trajectory plots|
|z bounds|The bounds of the z axis on the trajectory plots|
|equal aspect|Should the axes of the trajectory plots be equal scaling. (**default: True**)|

## vertical lines
|key|description|
|---|---|
|read from file|Should boundary crossings be read from file|
|file path|The path to the file to read boundary crossings from. Should be a csv file in the format of a pandas dataframe.|
|file line colour|Colour of boundary crossing vertical lines. (**default: red**)|
|labels|Labels for manually placed vertical lines. In the format of ["Label1","label2",...["labelN"]]|
|positions|Positions of manually placed vertical lines. In the format of ["position1", "position2",... "positionN"], where each position follows the format YYYY-MM-DDTHH:MM:SS. Leave as [] for no vertical lines|
|colours|Colours for each manually placed line to allow for different colours for each line. Must be in the format ["colour1", "colour2",... "colourN"]|
|linestyle|The matplotlib linestyle of the vertical lines. (**default: --** i.e. dashed)|

