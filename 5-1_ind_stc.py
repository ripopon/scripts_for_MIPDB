##import library
import matplotlib.pyplot as plt
import os
import os.path as op
import gc
import glob

import mne
from mne.datasets import fetch_fsaverage


def main():


    ##import fwd
    fwd = mne.read_forward_solution(fwd_path)

    ##epo_dir内の年齢ごとのフォルダを取得
    age_paths = glob.glob(epo_dir+'\*')
    
    for i in age_paths:
        epofolder_names = glob.glob(i+'\*')

        for j in epofolder_names:
                file_dir = j
                epofile_names = glob.glob(j+'\*')
                
                for file_name in epofile_names:
                    print(file_name)
                    
                    if epo_type in file_name and file_type in file_name:
                        try:
                            ##epoch dataのインポート
                            epochs = mne.read_epochs(file_name)
                            fig1 = epochs.plot(scalings='auto', picks='eeg', n_channels=5,show=False)
                            fig1.savefig(file_name.replace('epo.fif','epo.png'))
                            ##evoked data作成
                            evoked = epochs.average().pick('eeg')
                            fig1 = evoked.plot(time_unit='s',show=False)
                            fig1.savefig(file_name.replace('epo.fif','evo.png'))
                            plt.close('all')

                            ##covariance(共分散の計算)
                            cov = mne.compute_covariance(epochs, tmax=0., method=['shrunk', 'empirical'], rank=None, verbose=True)
                            ##cov.plot(epochs.info)


                            ##inverse operator
                            inv = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose=0.2)
                            
                            ##stc(source localization)
                            snr = 3.
                            lambda2 = 1. / snr ** 2
                            stc = mne.minimum_norm.apply_inverse(evoked, inv, lambda2,
                                                        method=method, pick_ori=None,
                                                        verbose=True)
                            
                            
                            save_dir = os.path.split(file_name)[0]+r'\stc'
                            if not os.path.exists(save_dir):
                                os.mkdir(save_dir)
                            

                            ##STC の範囲の絵画と保存
                            
                            plt.plot(1e3 * stc.times, stc.data[::100, :].T)
                            plt.xlabel('time (ms)')
                            plt.ylabel('%s value' % method)
                            png_file = save_dir+'\\'+os.path.split(file_name)[1].replace('_epo.fif','_%s_stc.png' % method)
                            plt.savefig(png_file,overwrite=True)
                            plt.close('all')
                            
                            ##STCfileの保存
                            stc_file = save_dir+'\\'+os.path.split(file_name)[1].replace('_epo.fif','_%s_stc' % method)
                            stc.save(stc_file)

                            del stc,inv,cov,evoked,epochs
                        except:
                            continue




                    
                    
"""
**CONFIG**
"""
epo_dir = r'E:\MIPDB\rest_eyeclose_20s'
fwd_path = r'E:\MIPDB\cmi_MIPDB_fwd.fif'
paradigm_type = '_Rest_'
tmax=20
data_type = 'rest_eyeclose_20s'
epo_type = 'Rest'
method = 'dSPM' ##or eLORETA  
file_type = 'epo.fif'
################################################

main()


 