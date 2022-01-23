"""
source power using DICS,beamformer,dSPM

"""

import os
import numpy as np
import glob

import mne




def _gen_mne(active_cov, baseline_cov, common_cov, fwd, info, method='dSPM'):
    inverse_operator = mne.minimum_norm.make_inverse_operator(info, fwd, common_cov)
    stc_act = mne.minimum_norm.apply_inverse_cov(active_cov, info, inverse_operator,
                                method=method, verbose=True)
    stc_base = mne.minimum_norm.apply_inverse_cov(baseline_cov, info, inverse_operator,
                                 method=method, verbose=True)
    stc_act /= stc_base
    return stc_act

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
                    try:
                        if epo_type in file_name and file_type in file_name:
                            
                            ##epoch dataのインポート
                            epochs = mne.read_epochs(file_name)

                            baseline_cov = mne.cov.compute_covariance(epochs,tmin=baseline_win[0],
                                                tmax=baseline_win[1],method='shrunk',rank=None)
                            active_cov = mne.cov.compute_covariance(epochs,tmin=active_win[0],
                                                tmax=active_win[1],method='shrunk',rank=None)
                            common_cov =baseline_cov+active_cov

                            ##active_cov.plot(epochs.info)

                            stc_dspm = _gen_mne(active_cov,baseline_cov,common_cov,fwd,epochs.info)

                            ##STCfileの保存
                            save_dir = os.path.split(file_name)[0]+r'\source_power'
                            print(save_dir)
                            if not os.path.exists(save_dir):
                                os.mkdir(save_dir)

                            stc_file = save_dir+'\\'+os.path.split(file_name)[1].replace('_epo.fif','_sourcepower_%s_stc' % method)
                            stc_dspm.save(stc_file)

                    
                    except:
                        continue

"""
**CONFIG**
"""
epo_dir = r'E:\MIPDB\MIPDB_video_3'
fwd_path = r'E:\MIPDB\cmi_MIPDB_fwd.fif'
epo_type = 'V3'
method = 'dSPM' ##or eLORETA 
file_type = 'epo.fif'
active_win = (0,20)
baseline_win = (-0.2,0)
##########################################
main()