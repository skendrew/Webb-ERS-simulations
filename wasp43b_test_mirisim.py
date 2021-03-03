import numpy as np
import matplotlib.pyplot as plt
import pdb
import glob

from mirisim.config_parser import SimulatorConfig, SimConfig, SceneConfig
from mirisim import MiriSimulation
from mirisim.skysim import ExternalSed, Background, Point


# in this script I'm going to take one output spectrum from exonoodle, and produce a very simple exposure with ngroups of 65

noodle_folder = 'output_bb_noLD/Noodles_2021-02-26/'

# load in a list of the files in the output folder
files = glob.glob(noodle_folder+'*.dat')
print('{} files found'.format(len(files)))

target = Point(Cen=(0., 0.))

# let's pick file 8 which is in eclipse for SED, and assign to target
sed = ExternalSed(sedfile=files[8])
target.set_SED(sed)

bg = Background(level='low', gradient=0., pa=0.)
scene = target + bg    

# create the target list for the scene file, make the scene and write out to file
targetlist = [target]
scene_config = SceneConfig.makeScene(loglevel=0, background=bg, targets=targetlist)
scene_file = 'wasp43b_simple_scene.ini'
scene_config.write(scene_file)

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
sim_config.write(simout)
	
# set up the simulator "under the hood". deafult values can be accepted here.
simulator_config = SimulatorConfig.from_default()


sim = MiriSimulation.from_configfiles(simout)
sim.run()


