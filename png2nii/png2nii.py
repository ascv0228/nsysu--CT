# for i in test_list:
#     file = i + '.nii.gz'
#     print(file)
#
#     datapath = NiiDataPath + file  # 檔案路徑
#     img = nib.load(datapath)  # 讀取Nii檔
#     img_arr = img.get_fdata()  # 從Nii 取得陣列
#     affine = img.affine.copy()  # 複製原Nii格式
#     hdr = img.header.copy()  # 複製原Nii格式
#     createDir = SaveProcessNiiPath_test + file
#
#     mkdir(createDir)
#
#
#     # 建立 Hu nii
#     HU_nii = nib.Nifti1Image(img_arr, affine=affine, header=hdr)
#     nib.save(HU_nii, os.path.join(createDir,  file))

from matplotlib import pyplot as plt
import nibabel as nib
import skimage.io as io
import numpy as np
import pandas as pd
import os
import glob
import shutil
from PIL import Image

import matplotlib.pyplot as plt  # plt 用于显示图片
ImgDataPath = 'D:\CAC_project\png2nii\datasets\ImgData/'
NiiDataPath = 'D:\CAC_project\png2nii\datasets\Origin-Nii/'
SaveProcessNiiPath = 'D:\CAC_project\png2nii\datasets\Create-Nii_D/'

WW = 350    # Hu值的 Window Width
WL = 30     # Hu值的 Window Level

# back_string = '_fake_B.png'
back_string = '.png'

all_nii_gz = os.listdir(NiiDataPath)
case_list = []
for i in all_nii_gz:
    if i.endswith('.nii.gz'):
        case_list.append(i[:-7])

ImgDataList = os.listdir(ImgDataPath)
case_list = list(set(case_list) & set(ImgDataList))


def getOriginAffine(FileName):
    file = FileName + '.nii.gz'
    datapath = NiiDataPath + file  # 檔案路徑
    img = nib.load(datapath)  # 讀取Nii檔
    img_arr = img.get_fdata()  # 從Nii 取得陣列
    affine = img.affine.copy()  # 複製原Nii格式
    hdr = img.header.copy()  # 複製原Nii格式
    return (affine, hdr)

def Hudistributed(img_arr, WW):
    HudistributedMatrix = np.copy(img_arr)
    HudistributedMatrix = HudistributedMatrix.astype('int32')

    # ============bigger than min value become -WW============
    # ============smaller than max value become WW============
    HudistributedMatrix[HudistributedMatrix > WW] = WW
    HudistributedMatrix[HudistributedMatrix < (-WW)] = -WW
    # ========================================================

    # ============bigger than WW value become max=============
    # ============smaller than WW value become min============
    # HudistributedMatrix[HudistributedMatrix > WW] = np.max(HudistributedMatrix)
    # HudistributedMatrix[HudistributedMatrix < (-WW)] = np.min(HudistributedMatrix)
    # ========================================================

    HudistributedMatrix = (HudistributedMatrix - np.min(HudistributedMatrix)) / (
                np.max(HudistributedMatrix) - np.min(HudistributedMatrix))
    HudistributedMatrix = HudistributedMatrix * WW - WW / 2
    HudistributedMatrix = HudistributedMatrix + WL
    print(np.max(HudistributedMatrix))
    return HudistributedMatrix

def getPngFileNameArray(FileName):
    length = len(FileName)
    back_length = len(back_string)
    disorder_img_list = glob.glob(ImgDataPath+FileName+'/*.png')
    disorder_img_list = [ss[len(ImgDataPath):] for ss in disorder_img_list]
    # print(disorder_img_list)
    order_number_list = list(map(str,sorted(map(int,[ss[2*length+2:-1*back_length] for ss in disorder_img_list]))))
    # print(order_number_list)
    order_img_list =[f'{ImgDataPath}/{FileName}/{FileName}_{ss}{back_string}' for ss in order_number_list]
    # print(order_img_list)
    return order_img_list

def getImgArray(FileName):
    order_img_list = getPngFileNameArray(FileName)
    allImg = np.zeros([512, 512, len(order_img_list)], dtype='int32')
    origin_img_arr = [np.asarray(Image.open(ii)) for ii in order_img_list]
    for i in range(0,len(origin_img_arr)):
        allImg[:, :, i] = origin_img_arr[i][:, :, 0]
    print(FileName, allImg.shape, allImg.dtype)
    return allImg * 400 // 255  # 0 ~ 255 to 0 ~ 400


def saveNiifromFileName(FileName):
    file = FileName + '.nii.gz'
    affine, hdr = getOriginAffine(FileName)
    img_arr = getImgArray(FileName)
    # Hunii = Hudistributed(img_arr, WW)
    print(np.max(img_arr))
    create_nii = nib.Nifti1Image(img_arr, affine=affine, header=hdr)
    # create_nii = nib.Nifti1Image(img_arr.astype('int32') * 400 // 255, affine=affine, header=hdr)
    nib.save(create_nii, os.path.join(SaveProcessNiiPath, file))

if not os.path.isdir(SaveProcessNiiPath):
    os.mkdir(SaveProcessNiiPath)

for i in case_list:
    saveNiifromFileName(i)
