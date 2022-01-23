"""
raw to epochs data

mne ver 0.21.0
Python ver 3.7.6
"""

##ライブラリインポート
import os
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

    ##epo_dir内の年齢ごとのフォルダを取得
    age_paths = glob.glob(epo_dir+'\*')
    for band in bands:
        for i in age_paths:
            age_range = os.path.split(i)[1]
            epofolder_names = glob.glob(i+'\*')
            evokeds = []

            for j in epofolder_names:
                    file_dir = j
                    epofile_names = glob.glob(j+'\*')
                    
                    for file_name in epofile_names:

                        try:
                            if file_type in file_name and band in file_name:
                                epoch = mne.read_epochs(file_name)
                                evokeds.append(epoch.average())
                            
                        except:
                            continue
            com_evokeds = mne.combine_evoked(evokeds,weights='nave')
            com_evokeds.nave = int(com_evokeds.nave)
            mne.evoked.write_evokeds(save_path+'\\group_{0}_{1}_ave.fif'.format(band,age_range),com_evokeds)

    ##すべてのデータのgroup
    age_paths = glob.glob(epo_dir+'\*')
    for band in bands:
        evokeds = []
        for i in age_paths:
            age_range = os.path.split(i)[1]
            epofolder_names = glob.glob(i+'\*')
            

            for j in epofolder_names:
                    file_dir = j
                    epofile_names = glob.glob(j+'\*')
                    
                    for file_name in epofile_names:

                        try:
                            if file_type in file_name and band in file_name:
                                epoch = mne.read_epochs(file_name)
                                evokeds.append(epoch.average())
                            
                        except:
                            continue
        com_evokeds = mne.combine_evoked(evokeds,weights='nave')
        com_evokeds.nave = int(com_evokeds.nave)
        mne.evoked.write_evokeds(save_path+'\\group_{0}_allage_ave.fif'.format(band),com_evokeds)
                



"""
**CONFIG**
"""
epo_dir = r'E:\MIPDB\MIPDB_video_3'
file_type = 'epo.fif'
save_path = epo_dir+'_groupevo'
bands = ('all','delta','theta','alpha','beta','gamma')
#############################################################

main()

