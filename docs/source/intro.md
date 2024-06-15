# Introduction

The **J**uno **U**niversal **P**lotting **T**ool is an all in one tool for creating and customising plots of many combinations of data from the Juno spacecraft, including magnetometer (MAG), radio wave (Waves), plasma (JADE) and Trajectory data.

The tool was developed and tested in Python 3.12, on unix-based operating systems.

## Motivation

The rapidly growing field of space physics lacks generalised tools with which to make the process of data visualisation both quick and easy for researchers.

This work shows the advantages of having user-friendly generalised tools in space physics, allowing researchers to spend less time on data visualisation and more time on science.

## Limitations

As of the current version, the tool does not function on Windows operating systems due to the automated use of wget in the scripts. It has, however, been tested fully using the Windows Subsystem for Linux (WSL).

The tool is limited in JADE-E (JADE Electron) data by the output on the NASA PDS (Planetary Data System), which only contains calibrated science outputs up to September 2021. Plots more recent than this will not function with JADE panels.
