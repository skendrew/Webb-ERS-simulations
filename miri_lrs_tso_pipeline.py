import numpy as np
import glob
import os
import matplotlib.pyplot as plt
import astropy.io.fits as fits

import jwst
from jwst.pipeline import Detector1Pipeline, Tso3Pipeline, Spec2Pipeline
from jwst.pipeline.collect_pipeline_cfgs import collect_pipeline_cfgs
from jwst.associations.asn_from_list import asn_from_list
from jwst.associations.lib.rules_level2_base import DMSLevel2bBase
from jwst.associations.lib.rules_level3_base import DMS_Level3_Base
import jwst.datamodels as datamodels

import pdb


sim_folder = 'wasp43_test_mirisim/'

print('changing into the simulation folder')
os.chdir(sim_folder)

ff =  'det_images/det_image_seq1_MIRIMAGE_P750Lexp1.fits'

# gather the config files bc TSOs need a dedicated config file
if not os.path.exists('../cfg_files/'):
    os.mkdir('../cfg_files/')
    cfgs = collect_pipeline_cfgs(dst='../cfg_files/')
	
# create an output directory if it doesn't yet exist
outdir = 'output_jwst{0}/'.format(jwst.__version__)
if not os.path.exists(outdir):
	os.mkdir(outdir)


# run detector1
d1 = Detector1Pipeline.call(ff,config_file='../cfg_files/calwebb_tso1.cfg', save_results=True, output_dir=outdir)

#pdb.set_trace()

# find the rateints file
ri_file = glob.glob(outdir+'*_rateints.fits')
assert len(ri_file) == 1, 'Cannot uniquely identify the rateints file! Please clean up your directory.'


# run the spec2pipeline with all default settings on the rateints file:
sp2 = Spec2Pipeline.call(ri_file[0], config_file='../cfg_files/calwebb_tso-spec2.cfg', save_results=True, output_dir=outdir)
print(sp2)


#pdb.set_trace()

calf = glob.glob(outdir+'*_calints.fits')
assert len(calf) == 1, 'Cannot uniquely identify the cal file! Please clean up your directory.'


asn = asn_from_list(calf, rule=DMS_Level3_Base, product_name='sp3_miri_tso')
with open('sp3_miri_tso_asn.json', 'w') as fp:
    fp.write(asn.dump()[1])



# run the Spec3pipeline with the calfile output from spec2
sp3 = Tso3Pipeline.call('sp3_miri_tso_asn.json', save_results=True)
print(sp3)

pdb.set_trace()

xfiles_sp2 = glob.glob(outdir+'*_x1dints.fits')

print(xfiles_sp2)
x1dm = datamodels.open(xfiles_sp2[0])

fig = plt.figure(figsize=[10,6])

for nn in range(x1dm.meta.exposure.nints):
    label = 'integration {0}'.format(nn)
    plt.plot(x1dm.spec[nn].spec_table['WAVELENGTH'], x1dm.spec[nn].spec_table['FLUX'], label=label)

plt.title('Spec2')

plt.legend()
fig.show()

xfiles_sp3 = glob.glob('sp3*_x1dints.fits')
print(xfiles_sp3)

x1dm3 = datamodels.open(xfiles_sp3[0])

fig = plt.figure(figsize=[10,6])

for nn in range(x1dm3.meta.exposure.nints):
    label = 'integration {0}'.format(nn)
    plt.plot(x1dm3.spec[nn].spec_table['WAVELENGTH'], x1dm3.spec[nn].spec_table['FLUX'], label=label)

plt.title('TSO3')
plt.legend()
fig.show()
