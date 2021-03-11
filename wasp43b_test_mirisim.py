# import numpy as np
# import matplotlib.pyplot as plt
# import pdb
# import glob

from mirisim.config_parser import SimulatorConfig, SimConfig, SceneConfig
from mirisim import MiriSimulation
from mirisim.skysim import ExternalSed, Background, Point

import rd_exonoodle as rdexon


def mirisim_exonoodle(sedfile,phase,overwrite=True):
    
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
    nint = 5
    nexp = 1
    
    simname = 'wasp43b_ers_shorttest'
    
    sim_config = SimConfig.makeSim(
        name = simname,    # name given to simulation
        scene = scene_file, # name of scene file to input
        rel_obsdate = 1.0,          # relative observation date (0 = launch, 1 = end of 5 yrs)
        POP = op_path,                # Component on which to center (Imager or MRS)
        ConfigPath = cfg,  # Configure the Optical path (MRS sub-band)
        Dither = False,             # Don't Dither
        StartInd = 1,               # start index for dither pattern [NOT USED HERE]
        NDither = 2,                # number of dither positions [NOT USED HERE]
        DitherPat = 'ima_recommended_dither.dat', # dither pattern to use [NOT USED HERE]
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
    # simulator_config = SimulatorConfig.from_default()
    
    
    sim = MiriSimulation.from_configfiles(simout)
    sim.run()
    
    return





#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Take output spectra from exonoodle, and produce a very simple exposure with ngroups of 65

noodle_folder = 'output_bb_noLD/Noodles_2021-02-26/'

# Read all exonoodle spectra or at a given phase:
# sedfiles, phases=rdexon.rd_exonoodle_filename(noodle_folder) # all phases
sedfiles, phases=rdexon.rd_exonoodle_filename(noodle_folder,phase_in=0.46666) # at a given phase; ~0 or ~1:transit and ~0.5:eclipse

#Run MIRISim with a simple setup
for sedfile, phase in zip(sedfiles, phases):
    print('Reading exonoodle spectrum at phase {}'.format(phase))
    # print(sedfile)
    mirisim_exonoodle(sedfile,phase,overwrite=True) #overwrites .ini files; turn it off by overwrite=Flase






