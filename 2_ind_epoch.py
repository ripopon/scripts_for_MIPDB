"""
make epoch file from raw file


"""
##import module
import os
import glob
import matplotlib.pyplot as plt

import mne
import mne.io as io
from mne.transforms import scaling
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


    def save_epoch(self,epoch,epoch_dir,file_dir,file_name,band,fmin,fmax,graphs=bool):
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
        epo_fname = epo_fname.replace('_raw.fif','%s_epo.fif' % band)
        epoch.save(epo_fname, overwrite=True)
        if graphs == True:
            fig1_name = epo_fname.replace('_epo.fif','_psd.png')    
            fig1 = epoch.plot_psd(fmin=fmin,fmax=fmax,average=True,spatial_colors=False,show=False)
            fig1.savefig(fig1_name)
            
            fig2_name = epo_fname.replace('_epo.fif','_topomap.png')   
            fig2 = epoch.plot_psd_topomap(bands=[(1,2,'delta'),(4,8,'Theta'),(8,12,'Alpha'),
                            (12,30,'Beta'),(30,45,'Gamma')],ch_type='eeg',show=False)
            fig2.suptitle(fig2_name)
            fig2.savefig(fig2_name)
            plt.close('all') 

            fig3_name = epo_fname.replace('_epo.fif','_epoim.png')   
            epoch.plot_image(picks='eeg',show=False,combine='mean')
            plt.savefig(fig3_name)
            
            fig4_name = epo_fname.replace('_epo.fif','_colorpsd.png')    
            fig4 = epoch.plot_psd(fmin=fmin,fmax=fmax,spatial_colors=True,show=False)
            fig4.savefig(fig4_name)

            plt.close('all') 
            
            ica=mne.preprocessing.ICA(n_components=10,method='fastica')
            ica.fit(epoch)
            ica.plot_components(show=False)
            plt.savefig(epo_fname.replace('_epo.fif','_ICA.png'))

            plt.close('all') 

        

class SourceLocalization():
    """
    source localizationを行う為のクラス
    """
    def __init__(self):
        pass

    def save_epo_evo_graphs(self,epoch,file_name,band,epoch_dir,file_dir,replace_name):
        os.chdir(epoch_dir)
        new_dir = os.path.split(file_dir)[1]
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        os.chdir(new_dir)
        epo_fname = os.path.split(file_name)[1]
        epo_fname = epo_fname.replace('_raw.fif',replace_name)
        print(epo_fname)

        fig1 = epoch.plot(scalings='auto', picks='eeg', n_channels=5, show=False)
        fig1.savefig(epo_fname.replace('_epo.fif','_%s_epo.png' % band))
        ##evoked data作成
        evoked = epoch.average().pick('eeg')
        fig2 = evoked.plot(time_unit='s',show=False)
        fig2.savefig(epo_fname.replace('_epo.fif','_%s_evo.png' % band))
        plt.close()
    
    def make_stc(self,epoch,method,fwd,file_name,epoch_dir,file_dir,replace_name):

        evoked = epoch.average().pick('eeg')

        ##covariance(共分散の計算)
        cov = mne.compute_covariance(epoch, tmax=0., method=['shrunk', 'empirical'], rank=None, verbose=True)


        ##inverse operator
        inv = mne.minimum_norm.make_inverse_operator(evoked.info, fwd, cov, loose=0.2)
        
        ##stc(source localization)
        snr = 3.
        lambda2 = 1. / snr ** 2
        stc = mne.minimum_norm.apply_inverse(evoked, inv, lambda2,
                                    method=method, pick_ori=None,
                                    verbose=True)

    
        os.chdir(epoch_dir)
        new_dir = os.path.split(file_dir)[1]
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        os.chdir(new_dir)
        epo_fname = os.path.split(file_name)[1]
        epo_fname = epo_fname.replace('_raw.fif',replace_name)

        ##STC の範囲の絵画と保存
        fig = plt.figure()
        plt.plot(1e3 * stc.times, stc.data[::100, :].T)
        plt.xlabel('time (ms)')
        plt.ylabel('%s value' % method)
        png_file = epo_fname.replace('_epo.fif','_%s_stc.png' % method)
        fig.savefig(png_file,overwrite=True)
        plt.close()
        
        ##STCfileの保存
        stc_file = epo_fname.replace('_epo.fif','_%s_stc' % method)
        stc.save(stc_file)

    





def main():

   
    ##import fwd
    fwd = mne.read_forward_solution(fwd_path)

    rest_dir = raw_dir.replace('MIPDB_raw',data_type)
    if not os.path.exists(rest_dir):
        os.mkdir(rest_dir)
    os.chdir(rest_dir)
    ##raw_dir内の年齢ごとのフォルダを取得
    age_paths = glob.glob(raw_dir+'\*')

    for i in age_paths:
        if any(map(i.__contains__, age_range)):##年齢のフィルタ
            rawfolder_names = glob.glob(i+'\*')
            restage_dir = i.replace('MIPDB_raw',data_type)
            if not os.path.exists(restage_dir):
                os.mkdir(restage_dir)
            
            for j in rawfolder_names:
                    file_dir = j
                    rawfile_names = glob.glob(j+'\*')
                    
                    for file_name in rawfile_names:
                    
                        if paradigm_type in file_name:
                            try:
                                ##raw import
                                print(file_name)
                                raw = RawData().raw_import(file_name)

                                ##event情報の取得
                                events = mne.find_events(raw,'STI 014')

                                ##epoching
                                epoch = RawData().make_epoch(raw,tmin=tmin,tmax=tmax,events=events,event_id=event_id,graph=False)
                            
                                ##filtering by Freq
                                epoch_delta = epoch.copy().filter(1,4)                       
                                epoch_theta = epoch.copy().filter(4,8)
                                epoch_alpha = epoch.copy().filter(8,13)                        
                                epoch_beta  = epoch.copy().filter(13,30)                           
                                epoch_gamma = epoch.copy().filter(30,45)
                                epochs = [epoch,epoch_delta,epoch_theta,epoch_alpha,epoch_beta,epoch_gamma]    
                                ##save epoch
                                replace_name = r'_epo.fif'
                                
                                bands = ['_all','_delta','_theta','_alpha','_beta','_gamma']
                                graphs = [True,False,False,False,False,False]
                                for epo,band,graph in zip(epochs,bands,graphs):
                                    RawData().save_epoch(epo,restage_dir,file_dir,file_name,band,
                                            fmin=1,fmax=45,graphs=graph)
                                
                                evoked = epoch.average()
                                fig1 = evoked.plot_topomap(times=(range(tmax)))
                                fig1.savefig(file_name.replace('MIPDB_raw',data_type).replace('raw.fif','topo.png'),overwrite=True)

                                plt.close('all') 

                                
                                


                            except:
                                import traceback
                                traceback.print_exc()
                                continue
                            
                            
                            
                                                                                                                                            
                                   
                            




"""
**CONFIG**
raw_dir  ：RawDataの保存されているディレクトリ（path）
age_range：下記範囲から選択
            ('6-9','10-11','12-13','14-17','18-24','25-44')
paradigm_type：paradigmの種類
    ('_Rest_', '_SL_', '_SyS_', '_SSB1_', '_CCB1_', '_CCB2_', '_CCB3_',
        '_SSB2_', '_V1_', '_V2_', '_V3_', '_V4_', '_V5_', '_V6_')
"""
raw_dir = r'E:\MIPDB\MIPDB_raw'
fwd_path = r'E:\MIPDB\cmi_MIPDB_fwd.fif'
paradigm_type = '_Rest_'
event_id={'rest_eyeopen':20} 
tmin=-0.2
tmax=20
data_type = 'rest_eyeopen_20s'
method='dSPM'
age_range = ('10-11','12-13','14-17','18-24')
####################################################

main()