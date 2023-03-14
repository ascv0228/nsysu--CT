import nibabel as nib
import os
from PIL import Image
import numpy as np
basePath = r"D:\CAC_project\no_noise_nii"
saveDir = "LDCT_data_png"
datasets = 'trainB' #trainA
CT_data = 'LDCT_data' #LDCT_data
# 路徑 ##############################################################################################################

# D:\CAC_project\LDCT_data_png

Save_path = f'{basePath}\{saveDir}'
# NiiDataPath = f'{basePath}\{CT_data}/'  # 原始的 Nii 檔  (不用改)
NiiDataPath =  r'D:\che\LDCT\BM3D\LDCT_nii_forBM3D_fix/'
NiiData = [r'10982384-L.nii.gz']
# listdir_ = os.listdir(NiiDataPath)
listdir_ = NiiData
# data = ['10982384-L.nii.gz']
for filename in listdir_:
    datapath = NiiDataPath + filename # 檔案路徑
    img = nib.load(datapath)    # 讀取Nii檔
    # img = nib.load(filename)
    img_arr = img.get_fdata()  # 從Nii 取得陣列
    Img_num = np.size(img_arr,2)
    if not os.path.isdir(Save_path):
        os.makedirs(Save_path)
    for i in range(Img_num):
        output = np.clip(img_arr[:, :, i], 0, 400)/400*255
        image = Image.fromarray(output)
        if image.mode == "F":
            image = image.convert('RGB')
        image.save('%s-%d.jpg'%(Save_path+'/'+filename[0:-7],i))
