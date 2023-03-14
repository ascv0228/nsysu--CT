import shutil
import os

# source=r'C:\Users\DelftStack\Documents\test\test.txt'
# destination=r'C:\Users\DelftStack\Pictures\test2\test2.txt'
# shutil.copyfile(source, destination)
source_path = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\total150/'
destination = r'D:\CAC_project\B083022053\temp2/'
new_source = r'D:\CAC_project\png2nii\datasets\Create-Nii/'
fs = os.listdir(source_path)
source_fs = list(map(lambda x : source_path+x, fs))
destination_fs = list(map(lambda x : destination+x, fs))

for f in fs:
    shutil.copy2(new_source+f, destination+f)
