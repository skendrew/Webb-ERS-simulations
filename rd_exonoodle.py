import numpy as np
import matplotlib.pyplot as plt


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions:
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rd_exonoodle(noodle_folder,phase_in=-1,tol=1e-5):
# reads exonoodle output files: either all or at a specific phase
# tol: how accurate the input phase should be
    data_time=np.genfromtxt(noodle_folder+'times.dat',skip_header=13)
    n_digits=len(str(len(data_time))) #number of files's digits to make file_index's format
    file_index,phase,time=data_time[:,0],data_time[:,1],data_time[:,2]

    exonoodle_spectra=[]
    if(0<=phase_in)&(phase_in<=1):
        print('Reading exonoodle spectrum at phase {}'.format(phase_in))
        # read spectrum at a specific phase
        near_bool,indx=find_nearest(phase, phase_in,tol)
        if(near_bool):
            i, p, t=file_index[indx], phase[indx],time[indx]
            
            f_ind="{:d}".format(int(i)).rjust(n_digits).replace(' ','0')
            data_spec=np.genfromtxt(noodle_folder+'SED_'+f_ind+'.dat',skip_header=12)
            dict_spec = {
                        "file": noodle_folder+'SED_'+f_ind+'.dat',
                        "phase": p,
                        "time": t,
                        "wavelength": data_spec[:,0],
                        "spectrum": data_spec[:,1]
                        }
            exonoodle_spectra.append(dict_spec)
        else:
            print('Phase NOT found! Choose a phase from:',phase)
            

    else:
        print('Reading exonoodle spectra at all phases ...')
        for i, p, t in zip(file_index, phase,time):
            f_ind="{:d}".format(int(i)).rjust(n_digits).replace(' ','0')
            data_spec=np.genfromtxt(noodle_folder+'SED_'+f_ind+'.dat',skip_header=12)
            dict_spec = {
                        "file": noodle_folder+'SED_'+f_ind+'.dat',
                        "phase": p,
                        "time": t,
                        "wavelength": data_spec[:,0],
                        "spectrum": data_spec[:,1]
                        }
            exonoodle_spectra.append(dict_spec)

    return exonoodle_spectra



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def rd_exonoodle_filename(noodle_folder,phase_in=-1,tol=1e-5):
# reads exonoodle output file names: either all or at a specific phase
# tol: how accurate the input phase should be
    data_time=np.genfromtxt(noodle_folder+'times.dat',skip_header=13)
    n_digits=len(str(len(data_time))) #number of files's digits to make file_index's format
    file_index,phase,time=data_time[:,0],data_time[:,1],data_time[:,2]

    exonoodle_files=[]
    phases=[]
    if(0<=phase_in)&(phase_in<=1):
        print('Reading exonoodle file name at phase {}'.format(phase_in))
        # read spectrum at a specific phase
        near_bool,indx=find_nearest(phase, phase_in,tol)
        if(near_bool):
            i, p, t=file_index[indx], phase[indx],time[indx]
            f_ind="{:d}".format(int(i)).rjust(n_digits).replace(' ','0')
            exonoodle_files.append(noodle_folder+'SED_'+f_ind+'.dat')
            phases.append(p)
        else:
            print('Phase NOT found! Choose a phase from:',phase)
    else:
        # reads all exonoodle output files with time and phase stamp
        print('Reading exonoodle file names at all phases ...')
        for i, p, t in zip(file_index, phase,time):
            f_ind="{:d}".format(int(i)).rjust(n_digits).replace(' ','0')
            exonoodle_files.append(noodle_folder+'SED_'+f_ind+'.dat')
            phases.append(p)

    return exonoodle_files, phases


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def find_nearest(array, value,tol):
    #Check if values are almost equal. If yes, then what's the index? (for phase comparison)
    near_bool=False
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    if(any(np.abs(array - value)<=tol)):
        near_bool=True
    return near_bool,idx 


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def plt_exonoodle(exonoodle_spectra):
    cm = plt.get_cmap('plasma') #gist_rainbow
    N=len(exonoodle_spectra)
    for i,d in enumerate(exonoodle_spectra):
        wln,sed,phase=d["wavelength"],d["spectrum"],d["phase"]
        if(N>1):
            plt.plot(wln,sed,lw=.7,color=cm(float(i)/float(N-1)),label="{:.3f}".format(phase))
        else:
            plt.plot(wln,sed,lw=.7,label="{:.3f}".format(phase))
 
    plt.yscale('log')
    plt.legend(title='Phase',fontsize=5)
    plt.xlabel("Wavelength ($\mu$m)")
    plt.ylabel("flux ($\mu$Jy)")
    
    return





# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # How to use:

# # exonoodle output directory
# noodle_folder = 'output_bb_noLD/Noodles_2021-02-26/'

# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Examplea of reading exonoodle output file names with time and phase stamps

# # read all spectra
# # exonoodle_fname_all, phases=rd_exonoodle_filename(noodle_folder)
# # print(exonoodle_fname_all)
# # read spectrum at a specific phase
# exonoodle_fname_singlephase, phases=rd_exonoodle_filename(noodle_folder,phase_in=0.46666)
# print(exonoodle_fname_singlephase)


# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Examplea of reading exonoodle output files with time and phase stamps

# # read all spectra
# exonoodle_spectra_all=rd_exonoodle(noodle_folder)
# # read spectrum at a specific phase
# exonoodle_spectra_singlephase=rd_exonoodle(noodle_folder,phase_in=0.46666)


# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # Plot all exonoodle output files
# plt_exonoodle(exonoodle_spectra_singlephase)
# plt_exonoodle(exonoodle_spectra_all)




