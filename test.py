##import module
import os
import glob
import matplotlib.pyplot as plt

import mne
import mne.io as io
from mne.viz.utils import plt_show
from numpy.core.fromnumeric import shape
from pandas import DataFrame


fwd_path = r'E:\MIPDB\cmi_MIPDB_fwd.fif'
fwd = mne.read_forward_solution(fwd_path)

print(fwd)

epoch=mne.read_epochs(r'E:\MIPDB\rest_eyeclose\14-17\A00056762\bp_A00056762_Rest_all_epo.fif')

evoked = mne.read_evokeds(r'E:\MIPDB\rest_eyeopen_groupevo\group_all_allage_ave.fif')
ica=mne.preprocessing.ICA(n_components=15,method='fastica')
ica.fit(evoked)
ica.plot_components()
