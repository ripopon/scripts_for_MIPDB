"""source power data contrast A/B
========================================

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

def main():

    if not os.path.exists(contrast_stc_foulder):
        os.mkdir(contrast_stc_foulder)

    file_list1 = sorted(set(i[:-7] for i in glob.glob(group_stc_foulder1+'\*.stc')))
    file_list2 = sorted(set(i[:-7] for i in glob.glob(group_stc_foulder2+'\*.stc')))


    for stc_path1,stc_path2 in zip(file_list1,file_list2):
        stc1 = mne.read_source_estimate(stc_path1)
        stc2 = mne.read_source_estimate(stc_path2)
    
        data = stc1.data-stc2.data

        stc = mne.SourceEstimate(data, stc1.vertices,stc1.tmin, stc1.tstep)
        stc.save(contrast_stc_foulder+'\\'+os.path.split(stc_path1)[1][5:]+'_contrast_'+condition,ftype='stc')


"""
**CONFIG**
"""
group_stc_foulder2 = r'E:\MIPDB\MIPDB_video_3_group_sourcepower'
group_stc_foulder1 = r'E:\MIPDB\rest_eyeopen_20s_group_sourcepower'


condition = 'EO-V3'

contrast_stc_foulder = r'E:\MIPDB\MIPDB_EO-V3_contrast_sourcepower'




####################################################################

main()