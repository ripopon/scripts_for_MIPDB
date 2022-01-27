import os
import os.path as op
import h5py
import pandas as pd
import numpy as np

import mne
import mne.io as io
from mne.datasets import fetch_fsaverage

class DataImport():
    """
    「hdf5からデータを抽出するためのクラス」\n
    CMI_MIPDBデータの保存形式であるmat(hdf5)から必要なデータを抽出する
    """
    def __init__(self): 
        pass
    
    def print_all_files(self,file_name):
        """
        hdf5ファイル構造の取得\n
        PARAMETER
        ----------
        file_name:展開するmatfile
        """
        def PrintOnlyDataset(name, obj):
            if isinstance(obj, h5py.Dataset):
                print(name)
        
        with h5py.File(file_name,mode='r') as mat:
            mat.visititems(PrintOnlyDataset)

    def import_ch_label(self,file_name):
        """
        channel_labelの取得\n
        PARAMETER
        ----------
        file_name:展開するmatfileパス
        """
        with h5py.File(file_name,mode='r') as mat:

            
            chloc = mat['EEG/chanlocs/labels']
            ch_label = []
            for j in range(len(chloc)):
                st = chloc[j][0]
                obj = mat[st]
                str1 = ''.join(chr(i) for i in obj[:])
                ch_label.append(str1)

            print('LABELS \n'+
                f'length: {len(ch_label)}'+'\n'+f'labels: {ch_label}')
            return ch_label

    def import_badch(self,file_name):
        """
        bad_channelの取得\n
        PARAMETER
        ----------
        file_name:展開するmatfileパス
        """
        with h5py.File(file_name,mode='r') as mat:
            bad_ch = mat['man_badchans'].value

        return bad_ch

    def import_data(self,file_name):
        """
        eegdataの取得\n
        PARAMETER
        ----------
        file_name:展開するmatfileパス
        """
        with h5py.File(file_name,mode='r') as mat:
            data = mat['EEG/data'].value
            arr_data = np.array(data)
            print('DATA \n'+
                f'shape: {arr_data.shape}'+'\n'+f'data[0,:]: {data[0,:]}')
        return data
    
    def import_event_latency(self,file_name):
        """
        EVENT情報(time)の取得\n
        PARAMETER
        ----------
        file_name:展開するmatfileパス
        """
        with h5py.File(file_name,mode='r') as mat:
            event_duration = mat['EEG/event/latency'].value

            event = []
            for j in range(len(event_duration)):
                st = event_duration[j][0]
                obj = mat[st]
                str1 = ''.join(chr(i) for i in obj[:])
                event.append(str1)
        return event
    
    def import_event_type(self,file_name):
        """
        EVENT情報(type)の取得\n
        PARAMETER
        ----------
        file_name:展開するmatfileパス
        """
        with h5py.File(file_name,mode='r') as mat:
            event_duration = mat['EEG/event/type'].value

            event = []
            for j in range(len(event_duration)):
                st = event_duration[j][0]
                obj = mat[st]
                str1 = ''.join(chr(i) for i in obj[:])
                event.append(str1)
            
        return event



class Montage():
    """
    montageの作成、絵画、編集を行うクラス
    """
    def __init__(self):
        pass

    def make_montage(self,ch_file_dir,ch_label):
        """
        montageの作成\n
        PARAMETER
        ----------
        ch_file_dir : チャネルファイルのpath
        ch_label : chLABELデータ（DATAimportクラスにて取得）
        """

        os.chdir(ch_file_dir)
        ndf = pd.read_csv('MIPDB_channels.txt')

        df = pd.DataFrame()
        for i in ch_label:
            df = df.append(ndf[ndf['name']==i])
        df

        ch_names = df.name.to_list()
        pos = df[['x','y','z']].values
        dig_ch_pos = dict(zip(ch_names,pos))
        nasion = [0,9.071585155,-2.359754454]
        lpa = [-6.711765,0.040402876,-3.251600355]
        rpa = [6.711765,0.040402876,-3.251600355]
        montage = mne.channels.make_dig_montage(ch_pos=dig_ch_pos,nasion=nasion,lpa=lpa,rpa=rpa,coord_frame='head')

        return montage,ch_names
    
    def graph3D(self,montage):
        """
        montageの絵画（３D）\n
        PARAMETER
        ----------
        montage : montage　data
        """
        montage.plot(kind='3d')
        print('enterで続行')
        input()
    
    def graph2D(self,montage):
        """
        montageの絵画（２D）\n
        PARAMETER
        ----------
        montage : montage data
        """
        montage.plot(kind='topomap')
        print('enterで続行')
        input()
    


# Download fsaverage files(MRI平均データ)
fs_dir = fetch_fsaverage(verbose=True)
subjects_dir = op.dirname(fs_dir)

# The files live in:
subject = 'fsaverage'
trans = 'fsaverage' 
src = op.join(fs_dir, 'bem', 'fsaverage-ico-5-src.fif')
bem = op.join(fs_dir, 'bem', 'fsaverage-5120-5120-5120-bem-sol.fif')

##montage

ch_file_dir = r'G:\MNEpython_DOI\deepdata_lec\mne_python_sclipts\data_for_MIPDB'
mat_dir = r'E:\MIPDB\MIPDB_mat'
file_for_ch_label = r'E:\MIPDB\MIPDB_mat\25-44\A00062219\gip_A00062219001.mat'
eog_chan = {'E1':'eog','E8':'eog','E14':'eog','E21':'eog','E25':'eog','E32':'eog'}    

##保存用rawディレクトリの作成
raw_dir = mat_dir.replace('MIPDB_mat','MIPDB_raw')
if not os.path.exists(raw_dir):
    os.mkdir(raw_dir)

"""
##ファイル構成の確認
    DATAimport.print_all_files(file_for_ch_label)
"""    


##montage/ch_namesの作成
ch_label = DataImport().import_ch_label(file_for_ch_label)
montage,ch_names = Montage().make_montage(ch_file_dir,ch_label)
del ch_label






##データ読み込み
fname = r'E:\MIPDB\MIPDB_raw\10-11\A00051826\gp_A00051826_Rest_raw.fif'
raw = io.read_raw_fif(fname,preload=True).pick('eeg')
print(raw.info)

print(raw.ch_names)

#Ch_nameが対応しているか確認
print(montage.ch_names)

#MRIデータと電極位置を合わせる
raw.set_montage(montage)
raw.set_eeg_reference(projection=True)  # needed for inverse modeling




#MRIデータ（fsaverage）とEEGデータの電極位置を３D表示し確認（エラーが起こりやすい）
mne.viz.plot_alignment(
    raw.info, src=src, eeg=['original', 'projected'], trans=trans,
    show_axes=True, mri_fiducials=True, dig='fiducials')
print('enterで続行')
input()

##位置ずれがなければ次のステップへ

# fwdファイルの作成
fwd = mne.make_forward_solution(raw.info, trans=trans, src=src,
                                bem=bem,eeg=True, mindist=5.0, n_jobs=1)
print(fwd)

"""
# for illustration purposes use fwd to compute the sensitivity map
eeg_map = mne.sensitivity_map(fwd, ch_type='eeg', mode='fixed')
eeg_map.plot(time_label='EEG sensitivity', subjects_dir=subjects_dir,
            clim=dict(lims=[5, 50, 100]))
"""


##データのセーブ
os.chdir(r'E:\MIPDB')
mne.write_forward_solution('cmi_MIPDB_fwd.fif',fwd,overwrite=True)
