"""
stc data from indivisual to groop
========================================
-make group STC for each age-range(6)

"""
##import library
import matplotlib.pyplot as plt
import os
import os.path as op
import numpy as np
import gc
import glob

import mne
from mne.datasets import fetch_fsaverage
from mne.parallel import parallel_func

def morph_stc(stc_file):
    smooth = 10
    fsaverage_vertices = [np.arange(10242), np.arange(10242)]
    # Morph STCs
    morph_mat = None
    
    stc = mne.read_source_estimate(stc_file)
    ##morphed = mne.compute_source_morph(stc,subject_from='fsaverage',subject_to='fsaverage')

    ##morphed.save(stc_file.replace('stc','morph'),overwrite=True)
    print('now importing file \n'+stc_file)

    return stc


def main():
    

    if not os.path.exists(group_stc_foulder):
        os.mkdir(group_stc_foulder)
    ##epo_dir内の年齢ごとのフォルダを取得
    age_paths = glob.glob(stc_dir+'\*')

    for band in bands:
        for i in age_paths:
            age_range = os.path.split(i)[1]
            epofolder_names = glob.glob(i+'\*')
            file_list = []
        
            for j in epofolder_names:
                file_names = glob.glob(j+'\*')
                file_dir = j
                
                for p in file_names:
                    if '\\stc' in p:
                        stc_files = glob.glob(p+'\*')
                        for files in stc_files:
                            if '.stc' in files and band in files:
                                file_name = files[:-7]
                                file_list.append(file_name)
            print(file_list)

                    
            stcs = parallel(run_func(subject_name) for subject_name in file_list)
            print('now avaraging stcs')
            data = np.average([s.data for s in stcs], axis=0)
            stc = mne.SourceEstimate(data, stcs[0].vertices,stcs[0].tmin, stcs[0].tstep)
            stc.save(group_stc_foulder+'\\'+groupstc_name+'_'+band+'_'+age_range,ftype='stc')

"""
##### age range 18-44
    for band in bands:
        file_list = []
        for i in age_paths:
            if any(map(i.__contains__, age_range)):
                age_range = os.path.split(i)[1]
                epofolder_names = glob.glob(i+'\*')
                
            
                for j in epofolder_names:
                    file_names = glob.glob(j+'\*')
                    file_dir = j
                    
                    for p in file_names:
                        if '\\stc' in p:
                            stc_files = glob.glob(p+'\*')
                            for files in stc_files:
                                if '.stc' in files and band in files:
                                    file_name = files[:-7]
                                    file_list.append(file_name)
        print(file_list)

                
        stcs = parallel(run_func(subject_name) for subject_name in file_list)
        print('now avaraging stcs')
        data = np.average([s.data for s in stcs], axis=0)
        stc = mne.SourceEstimate(data, stcs[0].vertices,stcs[0].tmin, stcs[0].tstep)
        stc.save(group_stc_foulder+'\\'+groupstc_name+'_'+band+'_18-44',ftype='stc')
    print('fin')
"""

"""
**CONFIG**
"""
stc_dir = r'E:\MIPDB\MIPDB_video_3_5s'
group_stc_foulder = stc_dir+r'_groupstc'
groupstc_name = 'MIPDB_video_3_5s_group'
parallel, run_func, _ = parallel_func(morph_stc,n_jobs=1)
bands = ('all','delta','theta','alpha','beta','gamma')
age_filter = ('18-24','25-44')
####################################################################

main()
