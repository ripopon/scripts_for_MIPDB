##import module
import os
import mne
import glob
from mne.datasets import fetch_fsaverage
import matplotlib.pyplot as plt
"""
**CONFIG**
"""
stc_folder = r'E:\MIPDB\MIPDB_V3-EO_contrast_sourcepower'
stc_files = sorted(set(i[:-7] for i in glob.glob(stc_folder+'\*.stc')))

clim=dict(kind='value',lims=[7, 8.5, 10])
for stc_file in stc_files:
    

    stc = mne.read_source_estimate(stc_file)
    fs_dir = fetch_fsaverage(verbose=True)
    subjects_dir = os.path.dirname(fs_dir)

    """時間軸での３D"""
    brain_dspm = stc.plot(
        hemi='both', subjects_dir=subjects_dir, subject='fsaverage',
        time_label='dSPM source power'+stc_file,views=['lat', 'med','ros','cau'],clim=clim)
    ##brain_dspm.add_annotation('aparc', borders=False)
    brain_dspm.save_image(stc_file+'.png')
    plt.close('all')
    del stc
