# Basic Configuration

The config options for JUPT are contained in two separate files. One *static* file which is used for configuring paths (`directory_config.ini`). And one *dynamic* file which is used to define the plotting settings for each output (`default_config.ini`).

We describe the first as *static*, meaning that this file will not be changing from plot to plot; And the second as *dynamic*, as for each plot created, you should create a copy of `default_config.ini`, and customise it for that plot specifically.

This *dynamic* config file is what is passed as an argument to the tool, as descibed in the [usage](usage) section.

## directory_config.ini

This is a config file which should contain the necessary file paths required by the plotting tool.

### Data

`data directory` : A path pointing to the directory where the data will we automatically downloaded and stored. e.g. /home/user/jupt_data/

`spice directory` : A path pointing to a directory containing a spice metakernel to load for trajectories (and in the future, ephemeris) plotting. e.g. `/home/user/spice/`

The following structure is expected in this directory:

```
SPICE/
├─ juno/
│  ├─ metakernel_juno.txt
```

See [installation guide](installation)

If you do not have a metakernel, you can create one using this tool: [DIASPICETools](https://github.com/mjrutala/DIASPICETools)

`download new data` : If True, this option deletes all data files of that data type before attempting to download new data.

### Plotting

`save figure` : If True, the figure generate is not displayed in a new window and is instead saved to JUPT/JUPT/JUPT_output/ under the name of the input config file.

If False, the figure is opened in a new window to be resized and viewed. An option to save here is also available.

### Trajectories

`magnetosphere boundaries repo path` : A path pointing to where the [jupiter_magnetosphere_boundaries](https://github.com/DIASPlanetary/jupiter_magnetosphere_boundaries/) repo is downloaded. See [installation guide](installation)


## default_config.ini

This is a file containing the default configuration options to make a plot. This should be used to test if you have installed the tool correctly.

For future plots, we recommend having a unique plotting config file for each plot and creating a folder to contain these. 

The filename of a saved plot is the same as the name of the config file which is passed to the script. It is important to have input config files with unique names to easily know which input corresponds to what figure.

### Plotting

`start time` : At what universal time should the plot start. Must be in the format of **YYYY-MM-DDTHH:MM:SS**. Note that decimal seconds are not supported and will cause a crash.

`end_time` : At what universal time should the plot end. Must be in the format descibed above in **start_time**.

#### Panel Indices

The ordering of the panels in the figure is able to be customised. As well as selecting which panels to be plotted. Beside each field named **plot x** - where x is the type of panel - set as **0**: if the panel should not be plotted, or as increasing integers starting with **1** denoting the order the panels should be plotted in.
