#!/usr/bin/env python
#  -*- coding: utf-8 -*-
# Marine Martin-Lagarde (CEA-Saclay) -- 2020/01/15 -- V2.0
# marine.martin-lagarde@cea.fr
#
# Python 3

"""
This file is a script from exonoodle package. It will plot the light-curve contained in the 'working directory', at a
certain 'wavelength'.
Inside the exonoodle result directory, it creates a 'lightcurve/' folder that will contain the light-curves.
"""

import matplotlib.pyplot as plt
from astropy.io import ascii
import numpy as np
import os
import sys
import pdb

working_directory = "wasp43b_ersspectra_bb_noLD/Noodles_2021-03-26"
wavelength = 7.5  # micron
show = False


# ----------------------------------------------------------------------------------------------


def find_nearest(array, value):
    """
    From https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array
    Find the closest value from 'value' in the array. Sending back the value from the array, and the corresponding
    index.

    :param array: np.array(float)
    :param value: float
    :return: array[idx]: float
    :return: idx: the index
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


def progress_bar(value, end_value, message="", bar_length=20):
    """
    Progress bar from exonoodle.utils, to show progress of a loop

    :param value: float - value that iterates
    :param end_value: float - end value when 'value' reaches 100%
    :param message: string - message to be printed before the progress bar [optional]
    :param bar_length: int - length of the bar
    """
    percent = float(value) / end_value
    arrow = '-' * int(round(percent * bar_length) - 1) + 'x'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r{0} [{1}] {2}%".format(message, arrow + spaces, int(round(percent * 100))))
    sys.stdout.flush()

# ----------------------------------------------------------------------------------------------


# GET TIME - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
time_file = os.path.join(working_directory, 'times.dat')
data = ascii.read(time_file)
phases = data["phase"].data
inds = data["file_index"].data
indexes = [int(ii) for ii in inds]
nb_points = np.size(phases)
padding = int(np.log10(nb_points)) + 1


pdb.set_trace()

# CREATE FILENAME ARRAY- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
SED_files = ["" for x in range(nb_points)]
for i in indexes:
    #SED_files[i] = os.path.join(working_directory, 'SED_{:0{}d}.dat'.format(i, padding))
    SED_files[i] = os.path.join(working_directory, 'SED_{:0{}}.dat'.format(i, padding))

# GET FLUXES - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
lightcurve = np.arange(nb_points)
data = ascii.read(SED_files[0])
cutout_wave, wave_index = find_nearest(data["wavelength"].data, wavelength)

for i in indexes:
    data = ascii.read(SED_files[i])
    lightcurve[i] = data["flux"].data[wave_index]
    progress_bar(i, max(indexes), "Looking in ..")


# CREATE PLOT  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fig = plt.figure(figsize=(20, 12), tight_layout=True)
plt.plot(phases, lightcurve, linewidth=3)
plt.title('LIGHTCURVE @ {}um'.format(cutout_wave))
plt.ylabel(r'Flux ($\mu$Jy)')
plt.xlabel('Orbital Phase')
plt.grid()
if show:
    plt.show()

folder_fig_path = os.path.join(working_directory, 'lightcurves')
os.makedirs(folder_fig_path, exist_ok=True)
fig_path = os.path.join(folder_fig_path, 'lightcurve_{}um.pdf'.format(wavelength))
fig.savefig(fig_path, dpi=fig.dpi, transparent=True, overwrite=True)
print("\nDone ! Find the file here: {}".format(fig_path))
