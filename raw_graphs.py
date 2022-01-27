##import module
import os
import glob
import matplotlib.pyplot as plt

import mne
import mne.io as io
from pandas import DataFrame

class RawData():
    """
    RawDATAのインポート編集を行う為のクラス
    """
    def __init__(self):
        pass

    def raw_import(self,fname):
        """
        import Rawdata from .fif file
        """
        picks = ('eeg','stim')
        raw = io.read_raw_fif(fname,preload=True).pick(picks)
        ##print(raw.info)
        return raw
    

    def make_epoch(self,data,tmin,tmax,events,event_id,graph=bool):
        """
        make eppoch data\n
        parameters
        -----------
        data : raw data

        tmin : 
        
        tmax : 
        """
        baseline=(0,0)

        ##epoch
        data.set_eeg_reference('average',projection=True)
        epoch_data = mne.Epochs(data,events=events,event_id=event_id,tmin=tmin,
                            tmax=tmax,baseline=baseline,reject=None)
        
        epoch_data.load_data()
        print(epoch_data)
        if graph==True:
            epoch_data.plot(scalings='auto',n_channels=5)
            epoch_data.plot_psd(fmin=1,fmax=45,average=True,spatial_colors=False)
            epoch_data.plot_psd_topomap(bands=[(1,4,'delta'),(4,8,'Theta'),(8,12,'Alpha'),
                    (12,30,'Beta'),(30,45,'Gamma')],ch_type='eeg')
        
        return epoch_data


    def save_epoch(self,epoch,epoch_dir,file_dir,file_name,replace_name):
        """
        epochdataの保存\n
        PARAMETER
        ----------
        '_epo.fif'
        """
        os.chdir(epoch_dir)
        new_dir = os.path.split(file_dir)[1]
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        os.chdir(new_dir)
        epo_fname = os.path.split(file_name)[1]
        epo_fname = epo_fname.replace('_raw.fif',replace_name)
        epoch.save(epo_fname,overwrite=True)

        fig1_name = epo_fname.replace('_epo.fif','_psd.png')    
        fig1 = epoch.plot_psd(fmin=1,fmax=50,average=True,spatial_colors=False,show=False)
        fig1.savefig(fig1_name)
        plt.close('all') 

        del epoch

def main():

    """
    raw_dir  ：RawDataの保存されているディレクトリ（path）
    age_range：下記範囲から選択
                ('6-9','10-11','12-13','14-17','18-24','25-44')
    paradigm_type：paradigmの種類
        ('_Rest_', '_SL_', '_SyS_', '_SSB1_', '_CCB1_', '_CCB2_', '_CCB3_',
            '_SSB2_', '_V1_', '_V2_', '_V3_', '_V4_', '_V5_', '_V6_')
    """
    raw_dir = r'E:\MIPDB\MIPDB_raw'
    paradigm_type = '_Rest_'
    event_id={'eye_close':20} 
    data_type = 'MIPDB_rest_eyeclose'
    tmax = 10

    rest_dir = raw_dir.replace('MIPDB_raw',data_type)
    if not os.path.exists(rest_dir):
        os.mkdir(rest_dir)
    os.chdir(rest_dir)
    ##raw_dir内の年齢ごとのフォルダを取得
    age_paths = glob.glob(raw_dir+'\*')

    for i in age_paths:
        rawfolder_names = glob.glob(i+'\*')
        restage_dir = i.replace('MIPDB_raw',data_type)
        if not os.path.exists(restage_dir):
            os.mkdir(restage_dir)
        
        for j in rawfolder_names:
                file_dir = j
                rawfile_names = glob.glob(j+'\*')
                
                for file_name in rawfile_names:
                    try:
                        if paradigm_type in file_name:
                        
                            raw = RawData().raw_import(file_name)
                            print(raw.info)
                            fig1_name = file_name.replace('.fif', paradigm_type+'.png')
                            fig1 = raw.plot(n_channels=20, scalings='auto',tmax=tmax, show=False)
                            fig1.suptitle(os.path.split(fig1_name)[1].replace('.png', ''))
                            fig1.savefig(fig1_name, overwrite=True)
                    except:
                        continue

main()
