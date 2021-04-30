import numpy as np
# import matplotlib.pyplot as plt
import pdb
import glob
import time
import resource
from functools import wraps


from mirisim.config_parser import SimulatorConfig, SimConfig, SceneConfig
from mirisim import MiriSimulation
from mirisim.skysim import ExternalSed, Background, Point

import rd_exonoodle as rdexon


import os


def mirisim_exonoodle(sedfile,phase,overwrite=True,nint=1, simname=None):
    
    target = Point(Cen=(0., 0.))

    sed = ExternalSed(sedfile=sedfile)
    target.set_SED(sed)
    
    bg = Background(level='low', gradient=0., pa=0.)
    # scene = target + bg    
    
    # create the target list for the scene file, make the scene and write out to file
    targetlist = [target]
    scene_config = SceneConfig.makeScene(loglevel=0, background=bg, targets=targetlist)
    scene_file = 'wasp43b_simple_scene.ini'
    scene_config.write(scene_file, overwrite=True) #change if overwrite is not desired
    
    # now set up the simulation parameters
    op_path = 'IMA'
    cfg = 'LRS_SLITLESS'
    filt = 'P750L'
    subarr = 'SLITLESSPRISM'
    
    # exposure configuration
    ngrp = 65
    # nint = 5
    nexp = 1
    
	#simname is now an input parameter
    #simname = 'wasp43b_ers_shorttest'
    
    sim_config = SimConfig.makeSim(
        name = simname,    # name given to simulation
        scene = scene_file, # name of scene file to input
        rel_obsdate = 1.0,          # relative observation date (0 = launch, 1 = end of 5 yrs)
        POP = op_path,                # Component on which to center (Imager or MRS)
        ConfigPath = cfg,  # Configure the Optical path (MRS sub-band)
        Dither = False,             # Don't Dither
        StartInd = 1,               # start index for dither pattern [NOT USED HERE]
        NDither = 2,                # number of dither positions [NOT USED HERE]
        DitherPat = 'lrs_recommended_dither.dat', # dither pattern to use [NOT USED HERE]
        disperser = 'SHORT',        # [NOT USED HERE]
        detector = 'SW',            # [NOT USED HERE]
        mrs_mode = 'SLOW',          # [NOT USED HERE]
        mrs_exposures = 10,          # [NOT USED HERE]
        mrs_integrations = 3,       # [NOT USED HERE]
        mrs_frames = 5,             # [NOT USED HERE]
        ima_exposures = nexp,          # number of exposures
        ima_integrations = nint,       # number of integrations
        ima_frames = ngrp,             # number of groups (for MIRI, # Groups = # Frames)
        ima_mode = 'FAST',          # Imager read mode (default is FAST ~ 2.3 s)
        filter = filt,          # Imager Filter to use
        readDetect = subarr         # Portion of detector to read out,
    )	
    
    # write the simulation config out to file, if out was set to True. the output filename is the simname, followed b the number of groups, ints and exp, for easy reference.
    simout = '{0}_simconfig.ini'.format(simname)
    sim_config.write(simout, overwrite=True) #change if overwrite is not desired
    	
    # set up the simulator "under the hood". deafult values can be accepted here.
    simulator_config = SimulatorConfig('erssim_simulator.ini')
    
    
    sim = MiriSimulation(sim_config, scene_config, simulator_config)
    sim.run()
    
    # now find the output folder and rename it
    for root, dirs, files in os.walk('./'):
        for dd in dirs:
            if 'mirisim' in dd:
                os.rename(dd, new_folder_name)
    
    
    return





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Take output spectra from exonoodle, and produce a very simple exposure with ngroups of 65

noodle_folder = 'exonoodle/wasp43b_ersspectra_finesamp/exonoodle_ersspectra_finesamp_exp1/'

# Read all exonoodle spectra or at a given phase:
sedfiles, phases=rdexon.rd_exonoodle_filename(noodle_folder) # all phases
print(sedfiles[:20], phases[:20])
#sedfiles, phases=rdexon.rd_exonoodle_filename(noodle_folder,phase_in=0.46666) # at a given phase; ~0 or ~1:transit and ~0.5:eclipse

#Run MIRISim with a simple setup
for sedfile, phase in zip(sedfiles[:3], phases[:3]):
    print('Reading exonoodle spectrum at phase {}'.format(phase))
    # print(sedfile)
    if(len(phases)>1):
        nint=1
    else:
        nint=5
    print('read spectrum {0}, phase {1:.5f}'.format(sedfile, phase))
    simname = 'wasp43b_ersspectra_finesamp_ph{0:.4f}'.format(phase)
    new_folder_name = 'wasp43b_ersspectra_finesamp_ph{0:.4f}_sim'.format(phase)
    #print(simname)
    #mirisim_exonoodle(sedfile,phase,overwrite=True,nint=nint, simname=simname) #overwrites .ini files; turn it off by overwrite=Flase
    
    # now find the output folder and rename it
#    for root, dirs, files in os.walk('./'):
#        for dd in dirs:
#            if 'mirisim' in dd:
#                os.rename(dd, new_folder_name)
    
    






