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
import glob
from src.dir_tool import *


def caculat_agatstone(NiiDataPath, MarkDataPath, case_name):
    datapath = NiiDataPath + case_name + '.nii.gz'  # 改檔名
    img = nib.load(datapath)
    img_arr = img.get_fdata()  # 取得影像陣列
    hdr = img.header.copy()  # 取得nii檔頭
    print(hdr['srow_z'][2])


if __name__ == '__main__':
    # 計算 Agatstone 分數
    NiiDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii_old/'
    # NiiDataPath = r'D:\che\Raw_Nii\SDCT_ToNII/'
    MarkDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii_old\label\Tang/'
    # case_name = "49978-G"
    case_name = "15702666-L"
    caculat_agatstone(NiiDataPath, MarkDataPath, case_name)   # test dataset
    # path = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\result/'
    # get_all_case(path)