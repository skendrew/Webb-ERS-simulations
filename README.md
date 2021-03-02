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





## Dependencies


