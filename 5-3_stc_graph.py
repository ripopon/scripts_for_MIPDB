##import module
import os
import mne
from mne.datasets import fetch_fsaverage
import matplotlib.pyplot as plt
"""
**CONFIG**
"""
initial_time = 0.2
pos_lims = [0.7, 0.9, 1.2] ##pngファイルから、推定
stc_file = r'E:\MIPDB\MIPDB_rest_eyeclose_groupdata\rest_eyeclose_group_all_18-44' ##file_path
movie_fname = stc_file+'_brain_movie'
#########################################################

stc = mne.read_source_estimate(stc_file)
fs_dir = fetch_fsaverage(verbose=True)
subjects_dir = os.path.dirname(fs_dir)


fig = plt.figure()
plt.plot(1e3 * stc.times, stc.data[::100, :].T)
fig.savefig(stc_file + r'.png')



"""時間軸での３D"""
brain = stc.plot(hemi = 'both',subject = 'fsaverage', subjects_dir = subjects_dir, initial_time = initial_time,
                clim = dict(kind='value', pos_lims=pos_lims), time_viewer=True)

##brain.save_movie(movie_fname, time_dilation=20, tmin=0, tmax=3,
##                    interpolation='linear', framerate=10)