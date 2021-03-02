#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run a exoNoodle simulation for a given exonoodle spectrum
"""
import exonoodle

#Initialisation of the variables
filename = "/Users/kendrew/sci_projects/exoplanets-ers/Webb-ERS-simulations/wasp43b_config.ini" # The filename with all the characteristics of your system

exonoodle.run(filename)
