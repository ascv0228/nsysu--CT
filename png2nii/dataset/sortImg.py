import nibabel as nib
import skimage.io as io
import numpy as np
import pandas as pd
import os
import glob
import shutil
from PIL import Image

ImgDataPath = r'D:\CAC_project\png2nii\datasets\ImgData/'
UnsortedImgDataPath = r'D:\CAC_project\png2nii\datasets\UnsortedImg/'
BasePath = r'D:\CAC_project\png2nii\datasets/'
Len = len(UnsortedImgDataPath)
all_nii_gz = os.listdir(r'D:\CAC_project\png2nii\datasets\Origin-Nii/')
f = open(r"D:\CAC_project\png2nii\datasets\ImgData\log2.txt", 'w+')
case_list = []
for i in all_nii_gz:
    if i.endswith ('.nii.gz'):
        case_list.append(i[:-7])

def arrangeImg(Filename):
    img_list = glob.glob(UnsortedImgDataPath+f'/{Filename}*.png')
    path = ImgDataPath+Filename
    if(not os.path.isdir(path)):
        os.mkdir(path)
    for g in img_list:
        print(g[Len:])
        os.replace(g, path+r'/' + g[Len:])

def writeFile(FileName):
    Len = len(os.listdir(ImgDataPath+FileName))
    print(f'{FileName} {Len}', file=f)

for i in case_list:
    arrangeImg(i)
    writeFile(i)