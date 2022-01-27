##import library
from mne.viz.utils import plt_show
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

import mne
from mne.datasets import fetch_fsaverage
from mne.minimum_norm import apply_inverse_epochs
from mne.connectivity import seed_target_indices, spectral_connectivity
from mne.viz import circular_layout, plot_connectivity_circle
from mne.parallel import parallel_func


fs_dir = fetch_fsaverage(verbose=True)
subjects_dir = os.path.dirname(fs_dir)

##Get Labels from fsaverage(FreeSuefer.annotfile)
labels = mne.read_labels_from_annot('fsaverage',parc='aparc',subjects_dir=subjects_dir)
labels = labels[0:68]
print(labels)


l = labels[51].pos.copy()

np.mean(l,axis=0)