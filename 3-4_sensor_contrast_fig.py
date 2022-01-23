##import library
import matplotlib.pyplot as plt
import os
import os.path as op
import glob

import mne
from mne.datasets import fetch_fsaverage

"""
**CONFIG**
"""
evokeds_dir = r'E:\MIPDB\MIPDB_contrast_V3-EO_groupevo'
file_type = 'ave.fif'
times = range(20)
##########################################

save_path = evokeds_dir+'\\topo'
if not os.path.exists(save_path):
    os.mkdir(save_path)

evoked_filenames = glob.glob(evokeds_dir+'\*')

for evoked_fname in evoked_filenames:
    if file_type in evoked_fname:
        print(evoked_fname)
        evokeds = mne.read_evokeds(evoked_fname,kind='average')

        fig1 = evokeds[0].plot_topomap(show=False,title=os.path.split(evoked_fname)[1],times=times)
        save_file = save_path+'\\'+os.path.split(evoked_fname)[1].replace('ave.fif','topo.png')
        fig1.savefig(save_file,overwrite=True)
        plt.close('all')
        
        ##times=times
        plt.psd(evokeds[0].data[0])
        plt.title('PSD {}'.format(os.path.split(evoked_fname)[1]).replace('ave.fif',''))
        save_file=save_path+'\\'+os.path.split(evoked_fname)[1].replace('ave.fif','psd.png')
        plt.savefig(save_file,overwrite=True)
        plt.close('all')

    
        




