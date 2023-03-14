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


datapath = r'D:\che\LDCT\BM3D\LDCT_nii_forBM3D/' +'15197827-L.nii.gz'  # 改檔名
d2 = r'D:\che\LDCT\BM3D\SDCT_nii_forBM3D/' +'15197827-P.nii.gz'

for i in (datapath, d2):
    img = nib.load(i)
    img_arr = img.get_fdata()  # 取得影像陣列
    hdr = img.header.copy()  # 取得nii檔頭
    print(hdr['pixdim'])