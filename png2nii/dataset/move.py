from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import skimage.io as io
import pandas as pd
import os
import glob
import shutil
import cv2 as cv
import time

org_folder = r"D:\CAC_project\png2nii\datasets\Create-Nii"
target_folder = r"E:\B083022053\deepmedic-master_New\examples\CTdatafortest\test"


for filename in os.listdir(org_folder):
    if ".nii.gz" in filename:
        org_file = f'{org_folder}\{filename}'
        target_p = f'{target_folder}\{filename}'
        target_f1 = f'{target_p}\{filename}'
        target_f2 = f'{target_p}\HU_{filename}'
        print(filename)
        # if not os.path.exists(target_p):
        #     os.mkdir(target_p)

        # shutil.copyfile(org_file, target_f1)
        # shutil.copyfile(org_file, target_f2)

