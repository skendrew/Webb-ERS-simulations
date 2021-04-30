#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob



"""
Run a exoNoodle simulation for a given exonoodle spectrum
"""
import exonoodle


#Initialisation of the variables

inp_files = glob('*_finesamp_*.ini')
print(inp_files)


#filename = "/Users/kendrew/sci_projects/exoplanets-ers/Webb-ERS-simulations/wasp43b_bb_ersspectra_noLD_config.ini" # The filename with all the characteristics of your system

for ff in inp_files:
    exonoodle.run(ff)
