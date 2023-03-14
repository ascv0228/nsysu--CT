from unittest import case
import nibabel as nib
import skimage.io as io
import numpy as np
import os
import shutil
from natsort import natsorted, ns
from skimage import measure,color
import pandas as pd
import matplotlib.pyplot as plt
import pydicom
import os
import glob
import csv

L_read_path = r'D:\che\LDCT\BM3D\LDCT_nii_forBM3D/'   # 改檔名
S_read_path = r'D:\che\LDCT\BM3D\SDCT_nii_forBM3D/'

def getOriginAffine(read_path, FileName):
    file = FileName + '.nii.gz'
    datapath = read_path + file  # 檔案路徑
    img = nib.load(datapath)  # 讀取Nii檔
    img_arr = img.get_fdata()  # 從Nii 取得陣列
    affine = img.affine.copy()  # 複製原Nii格式
    hdr = img.header.copy()  # 複製原Nii格式
    return (affine, hdr)

def getHdr(read_path, FileName):
    file = FileName + '.nii.gz'
    datapath = read_path + file  # 檔案路徑
    img = nib.load(datapath)  # 讀取Nii檔
    hdr = img.header.copy()  # 複製原Nii格式
    return hdr

# PixelSpacing_x = hdr['pixdim'][1]
# PixelSpacing_y = hdr['pixdim'][2]

all_dict = []
for path in [L_read_path, S_read_path]:
    all_nii_gz = os.listdir(path)
    case_list = []
    for i in all_nii_gz:
        if i.endswith('.nii.gz'):
            case_list.append(i[:-7])


    for i in case_list:
        hdr = getHdr(path, i)
        PixelSpacing_x = hdr['pixdim'][1]
        PixelSpacing_y = hdr['pixdim'][2]
        PixelSpacing_z = hdr['pixdim'][3]
        all_dict.append((i, PixelSpacing_x, PixelSpacing_y, PixelSpacing_z)) 

print(all_dict)


with open('patient_xyz.csv', 'w', newline='') as patient_height_file:
    writer = csv.writer(patient_height_file)
    writer.writerow(["Patient", "x", "y", "z"])
    for i in all_dict:
        try:
            writer.writerow([i[0],i[1],i[2],i[3]])
        except:
            continue




# for i in (datapath, d2):
#     img = nib.load(i)
#     img_arr = img.get_fdata()  # 取得影像陣列
#     hdr = img.header.copy()  # 取得nii檔頭
#     print(hdr['pixdim'])