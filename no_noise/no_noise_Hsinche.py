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

'''
test_img is your origin LDCT_Path
result_img is your output Path
'''

# test_img = r'D:\CAC_project\no_noise\test_img/'
# result_img = r'D:/CAC_project/no_noise/guass_2/'
# result_img = r'D:\CAC_project\no_noise\no-noise-3\test-result'
# test_img = r'D:\CAC_project\no_noise\case/'
# result_img = r'D:\CAC_project\no_noise\no-noise-3\result4/'
test_img = r'D:\CAC_project\pytorch-CycleGAN-and-pix2pix-master\datasets\trainA/'
# result_img = r'D:\CAC_project\no_noise\no-noise-3\cycle_gan/'
result_img = r'D:\CAC_project\no_noise\guass_result_new/'



kernel_size = 5           # guass kernal
sigma = 2                 # guass kernal
threshold = 95           # Binarize threshold
connect8_kernel_size = 3  # connect8_kernel_size
connect8_threshold = 140  # connect8_threshold
only_final = True         # Is only save final filter image

size = 512
back_string = '.png'
# start, end = 5, -5


dirPath = f'{result_img}{kernel_size}_{sigma}_{threshold}_{connect8_kernel_size}_{connect8_threshold}'
if not os.path.isdir(dirPath):
    os.makedirs(dirPath)

def getImgList(path):
    img_list = glob.glob(path + '/*.png')
    output = [i[len(path):] for i in img_list]
    return output

def getImgListbyCaseDict(ImgList):
    outputDict = dict()
    for i in ImgList:
        key = i[:i.find("_")]
        if key not in outputDict:
            outputDict[key] = [i]
        else:
            outputDict[key].append(i)
    
    return outputDict

def getOrderImgListbyCaseName(CaseName, ImgList, back_string):
    length = len(CaseName)
    back_length = len(back_string)
    # print(ImgList)
    # print([ss[length+1:-1*back_length] for ss in ImgList])
    order_number_list = list(map(str,sorted(map(int,[ss[length+1:-1*back_length] for ss in ImgList]))))
    # print(order_number_list)
    order_img_list =[f'{CaseName}_{ss}{back_string}' for ss in order_number_list]
    # print(order_img_list)
    return order_img_list

# 中值濾波
def median_filtering(img_array, n):
    filter_img = cv.medianBlur(img_array, n)
    return filter_img

# 高斯濾波
def gaussian_filtering(img_array, n, sigma):
    filter_img = cv.GaussianBlur(img_array, (n, n), sigma)
    return filter_img


# Canny 邊緣檢測(用不到)
def canny_edge_detect(img_array, low_th, up_th):
    edge = cv.Canny(img_array, low_th, up_th)
    return edge



# 銳化
def sharp(img_array):
    cv2.addWeighted(img, 1.5, blur_img, -0.5, 0)

def connect8(img_array):
    img_blur = cv.blur(img_array, (connect8_kernel_size,connect8_kernel_size))
    return img_blur > connect8_threshold

def FilterOrderImgList(Casename, OrderImgList, only_final):
    print("Start", Casename)
    cnt = 0
    Len = len(OrderImgList)
    
    for i in OrderImgList:
        img=np.array(Image.open(test_img + i).convert('L'), 'f')
        if not only_final: plt.imsave(f'{dirPath}/{i}',img, cmap='gray', vmin = 0, vmax = 255)
        new_img = np.zeros((512, 512), dtype=int)

        gaussian_img = gaussian_filtering(img, kernel_size, sigma)
        if not only_final: plt.imsave(f'{dirPath}/{i[:-4]}_gaussian_sigma.png', gaussian_img, cmap='gray', vmin=0, vmax=255)

        binarize_img = (gaussian_img > threshold)*255
        if not only_final: plt.imsave(f'{dirPath}/{i[:-4]}_binarize_mask.png', binarize_img, cmap='gray', vmin=0, vmax=255)


        connect8_img = connect8(binarize_img)  # True or False 
        if not only_final: plt.imsave(f'{dirPath}/{i[:-4]}_8connect_mask.png', connect8_img*255, cmap='gray', vmin=0, vmax=255)

        final_img = img*(connect8_img^False) + gaussian_img*(connect8_img^True)  # it's meaning {8connect 為 true， 使用原圖、8connect 為 false， 使用高斯濾波圖}
        # print((gaussian_img*(connect8_img^True)).tolist())
        if not only_final: plt.imsave(f'{dirPath}/{i[:-4]}_final_head.png', img*connect8_img, cmap='gray', vmin=0, vmax=255)
        if not only_final: plt.imsave(f'{dirPath}/{i[:-4]}_final_tail.png', gaussian_img*(connect8_img^True), cmap='gray', vmin=0, vmax=255)
        # print(np.sum(img*(connect8_img^False) >1))
        plt.imsave(f'{dirPath}/{i[:-4]}.png', final_img, cmap='gray', vmin=0, vmax=255)

        cnt += 1
        if cnt % 10 == 0 : print(cnt)
    else:
        return



img_list = getImgList(test_img)
img_list_by_case = getImgListbyCaseDict(img_list)
img_order_list_by_case = dict()
for i in img_list_by_case:
    img_order_list_by_case[i] = getOrderImgListbyCaseName(i, img_list_by_case[i], back_string)
    FilterOrderImgList(i, img_order_list_by_case[i], only_final)

