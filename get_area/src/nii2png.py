import nibabel as nib
import skimage.io as io
import numpy as np
import os
import shutil
from natsort import natsorted, ns
from skimage import measure,color
import pandas as pd
import matplotlib.pyplot as plt
import glob
from PIL import Image as im
import cv2


##############################################################################
# NiiDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii\label/'
# MarkDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\result\total60/'
# saveImgPath = r'D:\CAC_project\nii_and_mark_to_png\output/'
##############################################################################

def getOriginAffine(read_path, FileName):
    file = FileName + '.nii.gz'
    datapath = read_path + file  # 檔案路徑
    img = nib.load(datapath)  # 讀取Nii檔
    img_arr = img.get_fdata()  # 從Nii 取得陣列
    affine = img.affine.copy()  # 複製原Nii格式
    hdr = img.header.copy()  # 複製原Nii格式
    return (affine, img_arr, hdr)

def nii_to_png(NiiDataPath, saveImgPath, case_name):
    
    datapath = NiiDataPath  # 改檔名
    img = nib.load(datapath)
    img_arr = img.get_fdata()  # 取得影像陣列
    hdr = img.header.copy()  # 取得nii檔頭

    if(not os.path.isdir(saveImgPath)):
        os.makedirs(saveImgPath)
    
    
    for i in range(img_arr.shape[-1]):
        imgA = np.zeros((512, 512, 3))
        img = np.clip(img_arr[:,:,i], 0, 400) * 255 / 400
        imgA = img[:, :, None] * np.ones(3, dtype=int)[None, None, :]

        data = im.fromarray(np.uint8(imgA))
        # data.show()
        filename = saveImgPath + f'{case_name}_{i}.png'
        data.save(filename)

NiiDataPath = r'D:/che/LDCT/BM3D/SDCT_nii_forBM3D/12400474-P.nii.gz'
saveImgPath = r'D:/CAC_project/get_area/detail/12400474/SDCT/'
case_name = '12400474-P'
nii_to_png(NiiDataPath, saveImgPath, case_name)