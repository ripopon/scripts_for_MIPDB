・1_mat2raw_include_events.py
	|-matデータをrawデータに変換する。
	|-eventsのデータを[STI 014](stim channel)としてrawデータに付与。
	|-mne.find_events(raw,'STI 014')を用いてeventsデータを取得可能
	|-eventsデータを、用いてパラダイムを追跡可能

・2_ind_epoch.py
        |-rawデータからepochの作成
	|-関連するグラフを三枚保存（topomap[周波数/時間軸]、psd）
	|-epochは周波数ごとに作成
	
・3-1_group_sensor.py
        |-sensorレベルでのgroup解析を行う
	|-group evokedsデータの作成

・3-2_group_sensor_fig.py
        |-[3-1]で作成した[group evokeds]の絵画
	|-topo/psdが保存される

・3-3_sensor_contrast.py
        |-[3-1]で作成したファイルを用いて、contrastをとる
	|-2種のconditiionが必要

・3-4_sensor_contrast_fig.py
        |-[3-3]の絵画

・4-1_ind_source_power.py
        |-dSPMを用いて、source level解析を行う
	|-source powerの絵画に必要なSTCファイルを作成する
	|-周波数ごとに時間平均されたsourcepowerを見ることが可能

・4-2_group_source_power.py
        |-[4-1]のデータを元に複数被験者間のデータをgroup化する

・4-3_source_power_graph.py
        |-[4-1/4-2]のデータをグラフ化
	|-clim=dict(kind='value',lims=[0.1, 0.15, 0.2])   limsで閾値を変更可能
	|-上記１行を削除すると範囲が自動で決まる

・4-4_contrast_sourcepower.py
        |-[4-2]のデータ２種を用いてコントラストを計算する
	|-2種のconditiionが必要

・5-1_ind_stc.py
	|-Source localizationを行う
	|-この方法だと時間軸でデータを追うことが可能

・5-2_group_stc.py
	|-5-1データをグループ化する

・5-3__stc_graph.py
	|-5-1/5-2のグラフ化

・6-1_connectivity_circle.py
	|-connectivityの円グラフを作成する

・6-2_connectivity_toexcel.py
	|-excelファイルとしてconnnectivityを出力する。
	|-　横軸->縦軸への接続性

・make_fwd.py
FWDファイルの作成

###########「EVENTSの数値に対応するパラダイム」##############################################
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
###########################################################