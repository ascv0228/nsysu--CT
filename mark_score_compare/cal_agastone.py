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
import csv
from src.dir_tool import *

run = "8connect"
SDCT_xyz = [0.488281, 0.488281, 2.0]

def getWeight(HuValue, score_step=[130, 200, 300, 400, float ('inf') ]):
    if(len(score_step) < 5):
        score_step.append(float ('inf'))
    for i in range(len(score_step)):
        if(HuValue < score_step[i]):
            return i

# load offset
offset_fname = r'D:\CAC_project\B083022053\mark_score_compare\cum_by_offset\offset.csv'
offset_dict_from_csv = dict()
def load_offset():
    with open(offset_fname,newline='') as offset_file:
        reader = csv.DictReader(offset_file)
        for row in reader:
            offset_dict_from_csv[row['case_name']] = (int(row['pre_offset']),int(row['fol_offset']))
    return offset_dict_from_csv

def caculat_agatstone(NiiDataPath, MarkDataPath, case_name, score_step = [130, 200, 300, 400, float ('inf') ]):
    global run
    global offset_dict_from_csv
    if len(offset_dict_from_csv) == 0:
        load_offset()
    # list_result = getAllCaseName(NiiDataPath, '.nii.gz')
    # # natural sort 排序
    # # list_result = natsorted(list_result, key=lambda y: y.lower())  # .lower() 將英文大寫轉換為小寫

    # for i in list_result:
    # read original nii information
    datapath = NiiDataPath + case_name + '.nii.gz'  # 改檔名
    img = nib.load(datapath)
    img_arr = img.get_fdata()  # 取得影像陣列
    hdr = img.header.copy()  # 取得nii檔頭
    try:
        slice_thickness = round(hdr['srow_z'][2], 1)
        if slice_thickness < 1.5:
            slice_thickness = 2.5
    except:
        slice_thickness = 2.5
    # find pixel spacing
    PixelSpacing_x = hdr['pixdim'][1]  # 或  nii.header.get_zooms()
    PixelSpacing_y = hdr['pixdim'][2]  # 或  nii.header.get_zooms()
    PixelSpacing_z = img.header.get_zooms()
    # if PixelSpacing_x > 0.488282 or PixelSpacing_x < 0.488280:
    #     print(f'File : {case_name} ,  PixelSpacing = {PixelSpacing_x}')

    # read label information
    PredictLabelPath = getMarkDataPathbyCase(MarkDataPath, case_name) + '1.nii.gz'
    imgLabel = nib.load(PredictLabelPath)

    img_arrLabel = imgLabel.get_fdata()
    # Class1 = np.where(img_arrLabel == 1)
    # Class4 = np.where(img_arrLabel == 4)
    # Class5 = np.where(img_arrLabel == 5)
    Agatston = 0
    Agatston_z = 0
    Agatston_t = 0
    howmanycountPixel = 0
    sliceValue = 0
    Weight = 0
    pre_offset = offset_dict_from_csv.get(case_name, [0])[0]
    
    img_arrLabel = img_arrLabel[pre_offset: 512+pre_offset]

    for slice in range(img_arrLabel.shape[2]):
        Class1 = np.where(img_arrLabel[:, :, slice] == 1)  # 1為鈣化區  Class1為鈣化區的x,y座標
        imgShape = np.shape(img_arrLabel)
        Class1Image = np.zeros((imgShape[0], imgShape[1]))
        Class1Image[img_arrLabel[:, :, slice] != 1] = 0
        Class1Image[img_arrLabel[:, :, slice] == 1] = 1
        
        Class1Image[img_arr[:, :, slice] < score_step[0]] = 0
        # print(img_arr.shape)
        # print(img_arrLabel.shape)
        # print(Class1Image.shape)
        # xx = np.r_[np.zeros((4, imgShape[1])), img_arr[:, :, slice], np.zeros((1, imgShape[1]))]
        # print(xx.shape)
        # Class1Image[xx < 152] = 0

        # print(slice)
        # print(Class1!=[])
        if Class1[0].any() == True:  # any() : 如果都为空、0、false，则返回false(無發現鈣化)，如果不都为空、0、false，则返回true(有鈣化)。
            Class1 = list(Class1)

            # Class1=np.where(Class1[0]>64 and Class1[0]<384 and Class1[1]>256 and Class1[1]<384)
            # HuValue=0
            # countPixel=0


            if run == "8connect":
                # import matplotlib.pyplot as plt
                a = measure.label(Class1Image, connectivity=2)  # 對於二維來說，當connectivity=1時代表4連通，當connectivity=2時代表8連通

                # plt.imshow(a*255)
                # plt.show()

                for connect8 in range(1, a.max() + 1):  # a.max() >> 計算標註的label區塊數量
                    HuValue = 0
                    countPixel = 0
                    connect8Pixel = np.where(a == connect8)  # connect8Pixel = 鈣化pixel位置
                    ########################
                    # range1 = find(connect8Pixel, ymin=128, ymax=320, xmin=64, xmax=128) ## X垂直 Y水平
                    # range2 = find(connect8Pixel, ymin=64, ymax=384, xmin=128, xmax=256)
                    # range3 = find(connect8Pixel, ymin=128, ymax=384, xmin=256, xmax=320)
                    # range4 = find(connect8Pixel, ymin=192, ymax=320, xmin=320, xmax=384)
                    # combin12 = [np.append(range1[0], range2[0]), np.append(range1[1], range2[1])]
                    # combin123 = [np.append(combin12[0], range3[0]), np.append(combin12[1], range3[1])]
                    # combin1234 = [np.append(combin123[0], range4[0]), np.append(combin123[1], range4[1])]
                    # connect8Pixel = combin1234
                    ########################
                    for xAxis, yAxis in zip(connect8Pixel[0], connect8Pixel[1]):
                        Curr_HuValue = img_arr[xAxis, yAxis, slice]  # 依序取得每一個鈣化pixel的Hu值

                        if HuValue < Curr_HuValue:  # 保留最大Hu值
                            HuValue = Curr_HuValue
                        if Curr_HuValue >= score_step[0]:  # 避免"預測為鈣化,但Hu值卻小於130"
                            countPixel = countPixel + 1
                    Weight = getWeight(HuValue, score_step)
                    
                    Agatston_z = Agatston_z + Weight * countPixel * PixelSpacing_z[0] * PixelSpacing_z[1] * (
                                PixelSpacing_z[2] / 3)

                    Agatston = Agatston + Weight * countPixel * PixelSpacing_x * PixelSpacing_y * (slice_thickness / 3)
                    #   新累積分數 = 舊累積分數 + 權重 * 此slice的pixel數 * x方向縮放倍率 * y方向縮放倍率 * z方向縮放倍率
                    #   (2.5/3) 是醫師給定的數值

                    Agatston_t = Agatston_t + Weight * countPixel * PixelSpacing_x * PixelSpacing_y

    # print(howmanycountPixel)
    # print(case_name + '  Agatston Score : ', round(Agatston, 2))
    return round(Agatston, 2)

def agastone_class(agastone_score):
    
    try:
        if agastone_score == 0:
            return "No"
        elif agastone_score < 100:
            return "Low"
        elif agastone_score < 400:
            return "Middle"
        elif agastone_score < 1000:
            return "High"
        elif agastone_score > 1000:
            return "Higher"
    except:
        return "Error"

if __name__ == '__main__':
    # 計算 Agatstone 分數
    NiiDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii_old\label/'
    MarkDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii_old\label\Tang/'
    case_name = "11426463-L"
    caculat_agatstone(NiiDataPath, MarkDataPath, case_name)   # test dataset
    # path = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\result/'
    # get_all_case(path)