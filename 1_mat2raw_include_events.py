"""
convert eegdata from matfile(hdf5) to rawfile(mnepython)
=========================================================
-import eegdata from matfile(hdf5)
-make rawfile(mne-python)
-downsampling rawdata(500Hz->100Hz)
-add events to rawfile as [STI 014](ch_name)

"""

## import module
import os
import glob
import h5py
from mne import event
import pandas as pd
import numpy as np

import mne



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
    

        
class MakeRawData():
    """
    rawデータ作成の為のクラス
    """
    def __init__(self):
        pass

    def make_bad_ch_list(self,file_name,ch_names):
        """
        bad channelの指定を行う\n
        PARAMETER
        ----------
        file_name: bad_ch インポート元のmatfile
        ch_names: montageに含まれるch_name(make_montageにて作成)

        """
        bad = DataImport().import_badch(file_name)
        bad_ch = []
        for t in bad:
            bad_ch.append('E'+str(t).replace('[','').replace(']',''))
        bad_ch_in_chlist = set(ch_names) & set(bad_ch)
        return bad_ch_in_chlist

    def make_raw(self,ch_names,data,montage,eog_chan,bad_ch_in_chlist):
        """
        rawDataの作成\n
        PARAMETER
        ----------
        ch_names: rawデータに含まれるch名
        data: eegデータ
        montage: montageのデータ
        eog_chan: eog電極
        bad_ch_in_chlist: bad_chのデータ
        """
        info = mne.create_info(ch_names=ch_names, sfreq=500, ch_types='eeg')
        raw = mne.io.RawArray(data.T, info)
        raw.set_channel_types(eog_chan)
        raw.info['bads'] = list(bad_ch_in_chlist)
        raw.set_montage(montage)
        ##raw.plot(scalings='auto')
        return raw

    def save_raw(self,raw,raw_dir,file_dir,file_name):
        """
        rawdataの保存\n
        PARAMETER
        ----------
        raw: rawデータ
        raw_dir: 保存するrawデータのディレクトリ
        file_dir: 被験者毎のディレクトリ
        file_name: 保存名

        """
        os.chdir(raw_dir)
        new_dir = os.path.split(file_dir)[1]
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        os.chdir(new_dir)
        raw_fname = os.path.split(file_name)[1]
        raw_fname = raw_fname.replace('.mat','raw.fif')
        raw.save(raw_fname,overwrite=True)
        del raw

    def save_events(self,events,raw_dir,file_dir,file_name):
        """
        eventdataの保存（fif）\n
        PARAMETER
        ----------
        """
        os.chdir(raw_dir)
        new_dir = os.path.split(file_dir)[1]
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        os.chdir(new_dir)
        events_fname = os.path.split(file_name)[1]
        events_fname = events_fname.replace('.mat','-eve.fif')
        mne.write_events(events_fname,events)
        del events



def main():
    missed_list=[]
    ##各ディレクトリ
    """
    保存用ディレクトリ構成
    [MIPDB](保存用フォルダ)
        |-[MIPDB_targz]（ダウンロードデータ）
                |-[6-9]
                    |-[A00053375]
                    |-    .
                    |-    .
                |-[10-11]
                |-    .
                |-    .               
        |-[MIPDB_mat]（展開データ）
                |-~~~~~
        |-[MIPDB_raw]（RAWデータ）
                |-~~~~~

    big_dir: matdataの保存された
    """

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

    Montage().graph2D(montage)
    Montage().graph3D(montage)

    print(ch_names)

    """
    ##file_dir内のファイル名の取得
    age_paths = glob.glob(targz_path+'\*')
    ##print(age_paths)

    for i in age_paths:
        tarfile_names = glob.glob(i+'\*')

        for tarfile_name in tarfile_names:
            ##make [matfile_name] from [tarfile_name]
            matfile_name = tarfile_name[-16:-7]
            print(matfile_name)

            ##make [6-9][10-11]..... in [MIPDB_mat]
            matage_dir = i.replace('MIPDB_targz','MIPDB_mat')
            if not os.path.exists(matage_dir):
                os.mkdir(matage_dir)
            os.chdir(matage_dir)

            TarToMat(matfile_name,tarfile_name)
    """


    os.chdir(raw_dir)
    ##file_dir内のファイル名の取得
    age_paths = glob.glob(mat_dir+'\*')

    for i in age_paths:
        matfolder_names = glob.glob(i+'\*')
        rawage_dir = i.replace('MIPDB_mat','MIPDB_raw')
        if not os.path.exists(rawage_dir):
            os.mkdir(rawage_dir)

        for j in matfolder_names:

            file_dir = j
            matfile_names = glob.glob(j+'\*')

            for file_name in matfile_names:
                try:
                    print('\n now making {}'.format(file_name))

                    data = DataImport().import_data(file_name)
                
                    bad_ch_in_chlist = MakeRawData().make_bad_ch_list(file_name,ch_names)
                    raw = MakeRawData().make_raw(ch_names,data,montage,eog_chan,bad_ch_in_chlist)
                    
                    ## make [STI 014]
                    info = mne.create_info(['STI 014'], raw.info['sfreq'], ['stim'])
                    stim_data = np.zeros((1, len(raw.times)))
                    stim_raw = mne.io.RawArray(stim_data, info)
                    raw.add_channels([stim_raw], force_update_info=True)
                    
                    ## get events from matDATA
                    latency = DataImport().import_event_latency(file_name)
                    event_type = DataImport().import_event_type(file_name)
                    ascii_latency = []
                    int_event_type = []
                    for i in latency:
                        value = ord(i)
                        ascii_latency.append(value)
                    
                    for i in event_type:
                        value = int(i)
                        int_event_type.append(value)



                    ##eventsの取得、rawDATAへの付与
                    events = [ascii_latency, ['0']*len(event_type), int_event_type]
                    events = np.array(events,int).T
                    events[:,0] = events[:,0].astype(int)
                       
                    raw.add_events(events,'STI 014',True)
                    
                    ## ダウンサンプリング100Hz
                    raw_downsampled = raw.copy().resample(sfreq=100)
                    
                    ##event情報から、paradigmを取得、filenameを編集
                    
                    ## E:\MIPDB\MIPDB_mat\10-11\A00051826\gip_A00051826005.mat
                    paradigm_name = {90:'_Rest_', 91:'_SL_', 92:'_SyS_', 93:'_SSB1_', 94:'_CCB1_', 95:'_CCB2_', 96:'_CCB3_',
                                        97:'_SSB2_', 81:'_V1_', 82:'_V2_', 83:'_V3_', 84:'_V4_', 85:'_V5_', 86:'_V6_'}
                    paradigm_type = paradigm_name[events[0,2]]
                    
                    file_name_list = list(file_name)
                    file_name_with_event = "".join(file_name_list[:-7] + list(paradigm_type) + file_name_list[-4:])
                    
                    MakeRawData().save_raw(raw_downsampled,rawage_dir,file_dir,file_name_with_event)
                except:
                    print('\n missed {}'.format(file_name))
                    
                    missed_list.append(file_name)
                    continue
    print('we missed {}'.format(missed_list))


                



def test():
##各ディレクトリ
    """
    保存用ディレクトリ構成
    [MIPDB](保存用フォルダ)
        |-[MIPDB_targz]（ダウンロードデータ）
                |-[6-9]
                    |-[A00053375]
                    |-    .
                    |-    .
                |-[10-11]
                |-    .
                |-    .               
        |-[MIPDB_mat]（展開データ）
                |-~~~~~
        |-[MIPDB_raw]（RAWデータ）
                |-~~~~~

    big_dir: matdataの保存された
    """

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

    Montage().graph2D(montage)
    Montage().graph3D(montage)
    ##montage.save(r'E:\MIPDB\cmi_montage.fif')

   

try:
    main()
except:
    import traceback
    traceback.print_exc()



    """
    event_dict = {'start of Resting EEG paradigm': 90, 'eyes open start': 20, 'visual/left': 3,
              'visual/right': 4, 'smiley': 5, 'buttonpress': 32}
    Resting 1,2
    90: start of Resting EEG paradigm
    20: eyes open start
    30: eyes closed start

    Surround Suppression Paradigm
    93 = Surround Suppression Paradigm Block 1;
    97 = Surround Suppression Paradigm Block 2;
    4 = Stimulus ON
    8 = Stimulus OFF

    Sequence Learning Paradigm 3
    91 = Start of the Sequence Learning Paradigm
    11, 12, 13, 14, 15, 16, 17, 18 = DOT ON (12 and 17 are twice as often, because those stimuli appear twice within each block)
    21, 22, 23, 24, 25, 26, 27, 28 = DOT OFF (22 and 27 are twice as often, because those stimuli appear twice within each block)
    31, 32, 33, 34, 35 = new block

    Contrast Change Paradigm
    94 = Start Contrast Change Paradigm Block 1;    
    95 = Start Contrast Change Paradigm Block 2;
    96 = Start Contrast Change Paradigm Block 3;
    5 = start trial;
    8 = Target ON left;
    9 = Target ON right;
    12 = button press left;
    13 = button press right;

    Naturalistic Viewing Paradigm
    81 = Start of Video 1
    101 = Stop of Video 1
    82 = Start of Video 2
    102 = Stop of Video 2
    83 = Start of Video 3
    103 = Stop of Video 3

    Symbol Search Paradigm
    92 = Start of Symbol Search Paradigm;
    20 = Start of new page
    14 = response for trial
    
    Triggers for Start of the Paradigm:
    90 = Resting EEG
    91 = Sequence Learning Paradigm;
    92 = Symbol Search Paradigm;
    93 = Surround Suppression Paradigm Block 1;
    94 = Contrast Change Paradigm Block 1;    
    95 = Contrast Change Paradigm Block 2;
    96 = Contrast Change Paradigm Block 3;
    97 = Surround Suppression Paradigm Block 2;
    81 = Video1;
    82 = Video2;
    83 = Video3;
    84 = Video4;
    85 = Video5;
    86 = Video6;
events_name = {90:'R', 91:'SL', 92:'SyS', 93:'SSB1', 94:'CCB1', 95:'CCB2', 96:'CCB3',
                97:'SSB2', 81:'V1', 82:'V2', 83:'V3', 84:'V4', 85:'V5', 86:'V6'}
    """