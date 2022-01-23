"""
raw to epochs data

mne ver 0.21.0
Python ver 3.7.6
"""

##ライブラリインポート
import os
from mne.evoked import read_evokeds
import numpy as np
import mne
import mne.io as io
from pandas import DataFrame
import glob




"""
def main():
    num = '01'

    evokeds = make_groop_evoked(num)
    os.chdir(r'G:\MNEpython_DOI\deepdata_lec\mne_python_sclipts\DEAP_data_new\evokeds')
    evokeds_fname = 'eeg'+num+'groop-ave.fif'
    mne.evoked.write_evokeds(evokeds_fname,evokeds)
"""

'''
全データまとめて用
'''
def main():
    

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for band in bands:
        evo_data1 = evo_data_path1+r'\group_'+band+'_allage_ave.fif'
        evo_data2 = evo_data_path2+r'\group_'+band+'_allage_ave.fif'
        evoked1 = mne.read_evokeds(evo_data1)
        evoked2 = mne.read_evokeds(evo_data2)
        com_evokeds = evoked1.copy()
        com_evokeds[0].data = evoked1[0].data-evoked2[0].data
        mne.evoked.write_evokeds(save_path+'\\contrast_'+save_status+'_{0}_allage_ave.fif'.format(band),com_evokeds)
                



"""
**CONFIG**
"""
evo_data_path1 = r'E:\MIPDB\MIPDB_video_3_groupevo'
evo_data_path2 = r'E:\MIPDB\rest_eyeopen_20s_groupevo'


save_status = 'V3-EO'
##file_type = 'epo.fif'
save_path =  r'E:\MIPDB\MIPDB_contrast_V3-EO_groupevo'
bands = ('all','delta','theta','alpha','beta','gamma')
#############################################################

main()

