# Usage
This section presents a concise user's guide to running JUPT.

To run the tool, the following command must be run from the terminal:

```shell
python jupt.py CONFIG
```

**Positional arguments:**

* `CONFIG` : The relative path to the `.ini` config file corresponding to this plot. This can be the `default_config.ini` file, or a copy which has been configured as discussed in [Basic Configuration](basicConfig) and [Advanced Configuration](advancedConfig)


The tool will create a multipanel plot corresponding to this configuration file and (by default) save it as a `.png` under `JUPT/JUPT/JUPT_output` with the same filename as the input config file.
