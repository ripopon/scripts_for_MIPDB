import tarfile
import os
import glob

from numpy.lib.npyio import save


def TarToMat(matfile_name,tarfile_name):
    """
    Tar.gzからmatファイルを抽出する関数\n
    
    matfile_name : 保存するmatfile名
    tarfile_name : 抽出元のtarfile名
    """
    
    if not os.path.exists(matfile_name):
        os.mkdir(matfile_name)
    os.chdir(matfile_name)

    target_moji = 'EEG/preprocessed/mat_format'
    names = []
    members = []
    paths = []
    with tarfile.open(tarfile_name,'r') as tf:

        for mem in tf.getmembers():
            if target_moji in mem.name:
                paths.append(mem.name)
                members.append(mem)
        
        for path in paths:
            target = r'mat_format/'
            idx = path.find(target)
            name = path[idx+len(target):]
            names.append(name)
        ##print(names)
        
        
        for member,name in zip(members,names):
            f = tf.extractfile(member)
            with open(name,'wb') as c:
                c.write(f.read())
        
def main():
    os.chdir(r'E:\MIPDB')
    targz_path = r'E:\MIPDB\MIPDB_targz'

    if not os.path.exists('MIPDB_mat'):
        os.mkdir('MIPDB_mat')
 

    
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
    

try:
    main()
except:
    import traceback
    traceback.print_exc()

print('fin')



"""
保存用ディレクトリ構成
[MIPDB](保存用フォルダ)
    |-[MIPDB_targz]（ダウンロードデータ）
            |-[6-9]
                |-A00053375.tar.gz
                |-    .
                |-    .
            |-[10-11]
            |-    .
            |-    .               
    |-[MIPDB_mat]（展開データ）
            |-~~~~~
    |-[MIPDB_raw]（RAWデータ）
            |-~~~~~

"""