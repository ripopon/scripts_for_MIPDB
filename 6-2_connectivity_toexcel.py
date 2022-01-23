"""
make connectivity circle
"""

##import library
from re import L
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

def make_stc_from_epoch(epochs_file_name):
    """make stc"""
    ##import fwd
    fwd = mne.read_forward_solution(fwd_path)
    epochs = mne.read_epochs(epochs_file_name)
    ##evoked data作成
    evoked = epochs.average().pick('eeg')
    ##covariance(共分散の計算)
    cov = mne.compute_covariance(epochs, tmax=0., method=['shrunk', 'empirical'], rank=None, verbose=True)
    ##inverse operator
    inverse_operator = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose=0.2)

    snr = 1.0  # use lower SNR for single epochs
    lambda2 = 1.0 / snr ** 2
    method = "dSPM"  # use dSPM method (could also be MNE or sLORETA)
    stc_ind = apply_inverse_epochs(epochs, inverse_operator, lambda2, method,
                            pick_ori="normal", return_generator=True)
    return stc_ind

def make_con():
    
    con_all = dict()
    con_all_np = np.zeros((68,68))
    con_ind_np = np.zeros((68,68))
    con_list =[]
    """make src from inv"""
    ##import fwd
    fwd = mne.read_forward_solution(fwd_path)   
    ##epoch dataのインポート
    epochs = mne.read_epochs(sample_epoch_file_name)
    ##evoked data作成
    evoked = epochs.average().pick('eeg')
    ##covariance(共分散の計算)
    cov = mne.compute_covariance(epochs, tmax=0., method=['shrunk', 'empirical'], rank=None, verbose=True)
    ##inverse operator
    inv = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose=0.2)
    src = inv['src']
    del inv,cov,evoked,epochs

    ##epoch list
    age_paths = glob.glob(epo_dir+'\*')
    print(age_paths)
    file_list = []
    for i in age_paths:
        epofolder_names = glob.glob(i+'\*')
        print(epofolder_names)
        for j in epofolder_names:
            file_names = glob.glob(j+'\*')
            file_dir = j
            
            for files in file_names:
                if band+'_epo.fif' in files:
                    file_list.append(files)
    print(file_list)


    for file in file_list[0:1]:
        epochs_file_name = file
        stc = make_stc_from_epoch(epochs_file_name)
        
        ##Get Labels from fsaverage(FreeSuefer.annotfile)
        labels = mne.read_labels_from_annot('fsaverage',parc='aparc',subjects_dir=subjects_dir)
        ##labels = [labels[i] for i in label_list]
        labels=labels[0:68]
        print(labels)

        label_colors = [label.color for label in labels]
        label_ts = mne.extract_label_time_course(stc,labels,src,mode='mean_flip',
                                            return_generator=True)
        

        

        ##表示する、周波数帯の設定、connectivityの計算
        indices=((0,1),(1,0))
        fmin,fmax = bands_hz[band]
        con, freqs, times, n_epochs, n_tapers = spectral_connectivity(label_ts, method=con_methods, mode='multitaper', sfreq=sfreq, 
            fmin=fmin, fmax=fmax, faverage=True, mt_adaptive=True, n_jobs=1,tmin=tmin,tmax=tmax,indices=indices)


        con_ind = dict()
        for method, c in zip(con_methods, con):
            con_ind[method] = c[:, :, 0]

        if len(con_all)==0:
            con_all = con_ind.copy()
        else:
            for j in con_methods:
                con_all_np[:] = con_all[j]
                con_ind_np[:] = con_ind[j]
                con_all_np = (con_all_np+con_ind_np)/2
                con_all[j] = con_all_np
        
        con_res = con_all.copy()
        """
        ##label name の抽出
        label_to_excel = []
        for i in range(len(labels)):
            label_to_excel.append(labels[i].name)
        """
        
        with open(r'E:\data_for_MIPDB\labels.txt','r') as tf:
            label_to_excel =tf.read().split('\n')
        print(label_to_excel)
        ##condataの抽出
        con_imcoh = con_res['imcoh']

        df.update({band:pd.DataFrame(con_imcoh+con_imcoh.T,index=label_to_excel,columns=label_to_excel)})
        
        """
    """"""plot circle graph""""""
    label_names = [label.name for label in labels]

    lh_labels = [name for name in label_names if name.endswith('lh')]
    label_ypos = list()
    for name in lh_labels:
        idx = label_names.index(name)
        ypos = np.mean(labels[idx].pos[:, 1])
        label_ypos.append(ypos)

    lh_labels = [label for (yp, label) in sorted(zip(label_ypos, lh_labels))]
    rh_labels = [label[:-2] + 'rh' for label in lh_labels]
    node_order = list()
    node_order.extend(lh_labels[::-1])  # reverse the order
    node_order.extend(rh_labels)

    node_angles = circular_layout(label_names, node_order, start_pos=90,
                                group_boundaries=[0, len(label_names) / 2])


    for meth in con_methods:
        plot_connectivity_circle(con_res[meth], label_names, n_lines=n_lines,
                            node_angles=node_angles, node_colors=label_colors,
                            title='All-to-All Connectivity Condition {}'.format(meth) )
 

    ##make 2fig
    fig = plt.figure(num=None, figsize=(10, 6), facecolor='black')
    no_names = [''] * len(label_names)
    for ii, method in enumerate(con_methods):
        
        plot_connectivity_circle(con_res[method], no_names, n_lines=n_lines,
                                node_angles=node_angles, node_colors=label_colors,
                                title=method, padding=0, fontsize_colorbar=6,
                                fig=fig, subplot=(1, 3, ii + 1),show=False)
    plt_show()
        """



                    




        
       
    
    





"""
**CONFIG**
"""
##label_list = (2,3,4,5,6,7,10,11,14,15,18,19,28,29,46,47,50,51,58,59)
bands = ('all','delta','theta','alpha','beta','gamma')
bands_hz = {'all':(1,45),'delta':(1,4),'theta':(4,8),'alpha':(8,13),'beta':(13,30),'gamma':(30,45)}
connectivity_foulder = r'E:\MIPDB\MIPDB_video_3_connectivity'
if not os.path.exists(connectivity_foulder):
    os.mkdir(connectivity_foulder)

label_name = 'lh.aparc'

sample_epoch_file_name = r'E:\MIPDB\MIPDB_video_3\10-11\A00051826\oip_A00051826_V3_all_epo.fif'
fwd_path = r'E:\MIPDB\cmi_MIPDB_fwd.fif'
epo_dir = r'E:\MIPDB\MIPDB_video_3'

excel_name = connectivity_foulder+r'\MIPDB_video_3_group_connectivity_double.xlsx'


##connectivityの計算方法
con_methods = ['imcoh','pli','ciplv']

##表示範囲の指定
sfreq = 100.
n_lines = 20
tmin = 0.
tmax = 20.


##label:fsaverageのデータを使用
fs_dir = fetch_fsaverage(verbose=True)
subjects_dir = os.path.dirname(fs_dir)
fname_label = subjects_dir + '/fsaverage/label/%s.label' % label_name
label = mne.read_label(fname_label)
parallel, run_func, _ = parallel_func(make_stc_from_epoch, n_jobs=1)
df = {}

for band in bands:
    make_con()

with pd.ExcelWriter(excel_name) as writer:
    for band in bands:
        df[band].to_excel(writer,sheet_name=band)

