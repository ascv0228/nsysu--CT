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


version = 4

# nii 濾波資料夾
# NiiDataPath = f'D:/CAC_project/png2nii/datasets/Result/nii_data/{version}/'

# 標註資料夾
# MarkDataPath = f'D:/CAC_project/png2nii/datasets/Result/nii_data/{version}/Finish/'  #Result\Finish

outputXlsx = r'./agastone.cls'
outputPath = r''

suffix = '1.nii.gz'
run = "8connect"

def getAllCaseName(path, this_suffix):
    list_rst = os.listdir(path)
    list_result = []
    for names in list_rst:
        if names.endswith(this_suffix):
            list_result.append(names[:-len(this_suffix)])
    return list_result

def getMarkDataPathbyCase(MarkDataPath, case):
    return MarkDataPath + case + r'.nii_0_0_1\RoiVolume/'

def get_all_sub_dirs(path):
    dirs = os.listdir(path)
    for i in dirs:
        if not os.path.isdir(path + i):
            dirs.remove(i)
    else:
        return dirs

def get_all_case_by_sub_dirs(sub_dirs):
    return [ s[:s.rfind(".")] for s in sub_dirs]


def dict2Array2D(SDCT_Class_Dict):
    class_name = ["No", "Low", "Middle", "High", "Higher", "Error"]
    output_2DArray = [[],[],[],[],[],[]]
    for i in range(6):
        output_2DArray[i].append(SDCT_Class_Dict[class_name[i]]["Number"])
        if SDCT_Class_Dict[class_name[i]]["Number"] != 0:
            for j in range(6):
                output_2DArray[i].append(SDCT_Class_Dict[class_name[i]][class_name[j]]/SDCT_Class_Dict[class_name[i]]["Number"])

        else:
            for j in range(6):
                output_2DArray[i].append(0)
    return output_2DArray
