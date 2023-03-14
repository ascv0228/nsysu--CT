from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import skimage.io as io
import pandas as pd
import os
import glob
import shutil

def getImgList(path):
    img_list = glob.glob(path + '/*.png')
    output = [i[len(path):] for i in img_list]
    return output

test_img = r'D:\CAC_project\no_noise\case/'
result_img = r'D:\CAC_project\no_noise\result2/'
img_list = getImgList(test_img)
square = 5
sub_square = square//2
threshold = 20
cnt = 0

for i in img_list:
    img=np.array(Image.open(test_img + i).convert('L'), 'f') #打开图像并转化为数字矩阵
    new_img = np.zeros((512,512), dtype=int)
    # print(new_img.shape)
    for x in range(sub_square, 512-sub_square+1):
        for y in range(sub_square, 512-sub_square+1):
            sub_arr = img[x-sub_square:x+sub_square, y-sub_square:y+sub_square]
            temp = sub_arr.sum()//(square * (square - sub_square)) # - sub_square
            if temp > 100: temp *= 1.3
            if (np.std(sub_arr.tolist()) > threshold):
                new_img[x ,y] = temp
            else:
                new_img[x ,y] = img[x, y]

    plt.imsave(f'{result_img + i}',new_img, cmap='gray', vmin = 0, vmax = 255)
    cnt += 1
    if(cnt % 10 == 0): print(cnt)