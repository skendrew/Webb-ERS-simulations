# JWST MIRI Early Release Science Transiting Exoplanet simulations
simulations for the JWST ERS program

This repository contains scripts and data to perform MIRI simulations for the JWST Transiting Exoplanets Early Release Science Program. The aim is to produce products that are as scientifically representative as possible, to gain experience with the data products and analysis procedures. More information on the program and the MIRI component in particular can be found in the following publications:

* [Bean et al, 2018](https://ui.adsabs.harvard.edu/abs/2018PASP..130k4402B/abstract)
* [Venot et al, 2020](https://ui.adsabs.harvard.edu/abs/2020ApJ...890..176V/abstract)

## Packages used

The main packages used for these simulations are:

* exonoodle: produces synthetic transit, eclipse or phase curve spectra for given star & planet properties. Code and documentation can be found [here](https://gitlab.com/mmartin-lagarde/exonoodle-exoplanets).  See also the [JOSS paper by Martin-Lagarde et al 2021.](https://joss.theoj.org/papers/10.21105/joss.02287)
* MIRISim: produces simulated MIRI data for imager and spectroscopy modes. Publicly available from [this webpage](https://wiki.miricle.org/Public/MIRISim_Public).
* MIRISim\_tso: a MIRISim add-on package that take MIRISim simulations, packages them into a time series and adds time-dependent noise and drifts.

## Contents and structure of the repository

Last updated: 26 March 2021 -- SK

The contents of the repository are as follows:

#### Exonoodle files
* wasp43b\_exonoodle.py: a script that runs exonoodle to generate the synthetic spectra. 
* wasp43b\_bb\_noLD\_config.ini: the exonoodle configuration file that assumes the star is a simple BB (with the appropriate temperature and normalised to the correct magnitude).
* wasp43b\_bb\_ersspectra\_noLD\_config.ini: the exonoodle configuration file using the input values and spectra from the ERS team. 
* OUTPUT: output\_bb\_noLD: folder containing the exonoodle output spectra from the above run


#### Folder CEA
This contains the input spectra for WASP43b delivered with exonoodle. 

#### Folder TauREX
This contains the input spectra delivered by R. Challener of the transiting exoplanets ERS team, which will be used in common for all simulated datasets. Three spectra are used: daytime emission, nighttime emission and transmission. From teh original files we converted the the wavenumber axis into wavelengths (in micron), and wrote the table out in ECSV format, as required by exonoodle. 

#### MIRISim files (version used: 2.3.0)
* wasp43b\_test\_mirisim.py: short script to set up and run a single MIRISim run using *one* of the exonoodle output spectra
* wasp43b\_simple\_scene.ini: scene configuration file for MIRISim. This file is generated and written out in wasp43b\_test\_mirisim.py.
* wasp43b\_ers\_shorttest\_simconfig.ini: the simulation configuration file for a short test simulation. This file is generated and written out in wasp43b\_test\_mirisim.py.
* OUTPUT: wasp43\_test\_mirisim: folder containing the MIRISim output

#### Pipeline (version used: 0.18.3/Build 7.7)
* miri\_lrs\_tso\_pipeline.py: script that takes the MIRISim output and runs it through the JWST calibration pipeline
* OUTPUT: the pipeline output files are located in wasp43\_test\_mirisim/output\_jwst0.18.3/ (the pipeline output files are NOT in the repository)



## Dependencies

Check the individual packages for dependencies. These will most likely all be installed with the packages themselves.

In addition, the following packages are used in the scripts:
* glob
* os
* pdb (optional for debugging, these can be commented out)
* matplotlib
