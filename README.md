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
|||
|plot Waves|Should Waves data be plotted. Must be either **True** or **False**|
|plot MAG|Should MAG data be plotted. Must be either **True** or **False**|
|||
|panel spacing|The white space vertically between panels in units of panel height. (**default: 0**)|
|||
|~~font size~~|Base fontsize for the plot. Currently not functional due to **issue #9**|
|||
|||

Run `python jupt.py` to create the plot.

Note, the figure is not automatically saved.
