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
from PIL import Image as im
import cv2


##############################################################################
NiiDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii\label/'
MarkDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\result\total60/'
saveImgPath = r'D:\CAC_project\nii_and_mark_to_png\output/'
##############################################################################

all_case = get_all_case_by_sub_dirs(get_all_sub_dirs(MarkDataPath))

def nii_to_markImg_by_case(NiiDataPath, MarkDataPath, saveImgPath, case_name):
    
    datapath = NiiDataPath + case_name + '.nii.gz'  # 改檔名
    img = nib.load(datapath)
    img_arr = img.get_fdata()  # 取得影像陣列
    hdr = img.header.copy()  # 取得nii檔頭

    PredictLabelPath = getMarkDataPathbyCase(MarkDataPath, case_name) + '1.nii.gz'
    imgLabel = nib.load(PredictLabelPath)
    img_arrLabel = imgLabel.get_fdata()
    if img_arr.shape != img_arrLabel.shape:

        offset1 = (img_arrLabel.shape[0] - 512)//2
        offset2 = img_arrLabel.shape[0] - 512 - offset1
        img_arrLabel2 = img_arrLabel[offset1:-offset2,:,:]
        
        if img_arr.shape != img_arrLabel2.shape:
            print(case_name , ': img_arr.shape != img_arrLabel.shape : '+f'{img_arr.shape} != {img_arrLabel2.shape},  {img_arrLabel.shape}')
            return "ERROR"
        img_arrLabel = img_arrLabel2

    
    if(not os.path.isdir(saveImgPath + case_name)):
        os.mkdir(saveImgPath + case_name)
    
    
    for i in range(img_arrLabel.shape[-1]):
        imgA = np.zeros((512, 512, 3))
        img = img_arr[:,:,i] * 255 / 400
        imgA = img[:, :, None] * np.ones(3, dtype=int)[None, None, :]
        this_img_Label = img_arrLabel[:, :, i][:, :, None] * np.ones(3, dtype=int)[None, None, :]
        Class1Image = np.zeros((512, 512,3))
        Class1Image = ((this_img_Label[:, :] != np.ones(3)) * imgA[:, :]) + ((this_img_Label[:, :] == np.ones(3)) * np.array([[255. ,0. ,0.]]))

        data = im.fromarray(np.uint8(Class1Image))
        # data.show()
        filename = saveImgPath + case_name + '/' + f'{case_name}_{i}.png'
        data.save(filename)


for i in all_case:
    nii_to_markImg_by_case(NiiDataPath, MarkDataPath, saveImgPath, i)