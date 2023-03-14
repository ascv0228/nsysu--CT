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

# test_img = r'D:\CAC_project\no_noise\no-noise-3\test-img/'
# result_img = r'D:/CAC_project/no_noise/guass_result/'
# result_img = r'D:\CAC_project\no_noise\no-noise-3\test-result'
# test_img = r'D:\CAC_project\no_noise\case/'
# result_img = r'D:\CAC_project\no_noise\no-noise-3\result4/'
# test_img = r'D:\CAC_project\pytorch-CycleGAN-and-pix2pix-master\datasets\trainA/'
# result_img = r'D:\CAC_project\no_noise\no-noise-3\cycle_gan/'
# test_nii = r'D:\che\LDCT\BM3D\LDCT_nii_forBM3D_fix/'
result_img = r'D:\CAC_project\no_noise_nii\guass_result/'
test_nii = r'D:\CAC_project\no_noise_nii\LDCT_data_png/'



kernel_size = 5           # guass kernal
sigma =4                  # guass kernal
threshold = 100           # Binarize threshold
connect8_kernel_size = 3  # connect8_kernel_size
connect8_threshold = 140  # connect8_threshold
only_final = False         # Is only save final filter image

size = 512
back_string = '.png'
# start, end = 5, -5


dirPath = f'{result_img}NII_{kernel_size}_{sigma}_{threshold}_{connect8_kernel_size}_{connect8_threshold}'
if not os.path.isdir(dirPath):
    os.makedirs(dirPath)

# def getImgList(path):
#     img_list = glob.glob(path + '/*.png')
#     output = [i[len(path):] for i in img_list]
#     return output

def getNiiList(path):
    nii_list = glob.glob(path + '/*.nii.gz')
    output = [i[len(path):] for i in nii_list]
    return output

# def getImgListbyCaseDict(ImgList):
#     outputDict = dict()
#     for i in ImgList:
#         key = i[:i.find("_")]
#         if key not in outputDict:
#             outputDict[key] = [i]
#         else:
#             outputDict[key].append(i)
    
#     return outputDict

# def getOrderImgListbyCaseName(CaseName, ImgList, back_string):
#     length = len(CaseName)
#     back_length = len(back_string)
#     # print(ImgList)
#     # print([ss[length+1:-1*back_length] for ss in ImgList])
#     order_number_list = list(map(str,sorted(map(int,[ss[length+1:-1*back_length] for ss in ImgList]))))
#     # print(order_number_list)
#     order_img_list =[f'{CaseName}_{ss}{back_string}' for ss in order_number_list]
#     # print(order_img_list)
#     return order_img_list

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

def getOriginAffine(read_path, FileName):
    file = FileName + '.nii.gz'
    datapath = read_path + file  # 檔案路徑
    img = nib.load(datapath)  # 讀取Nii檔
    img_arr = img.get_fdata()  # 從Nii 取得陣列
    affine = img.affine.copy()  # 複製原Nii格式
    hdr = img.header.copy()  # 複製原Nii格式
    return (affine, img_arr, hdr)

def read_data_to_img_arr_list(img_arr):
    Img_num = np.size(img_arr,2)
    return [ Image.fromarray(img_arr[:,:,i]) for i in range(Img_num)]



def FilterNii(Casename, only_final):
    print("Start", Casename)
    cnt = 0
    affine, img_arr, hdr = getOriginAffine(test_nii, Casename)
    # start, end = (None, None) if (Len < 56) else (5, -5)
    
    img_list = read_data_to_img_arr_list(img_arr)
    if not os.path.isdir(f'{dirPath}/{Casename}'):
        os.makedirs(f'{dirPath}/{Casename}')
    if not os.path.isdir(f'{dirPath}/All/{Casename}'):
        os.makedirs(f'{dirPath}/All/{Casename}')
    for i in range(len(img_list)):
        img = np.array(img_list[i].convert('L'), 'f')
        # if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}.png',img/400*255, cmap='gray', vmin = 0, vmax = 255)
        if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}.png',img, cmap='gray', vmin = 0, vmax = 255)

        gaussian_img = gaussian_filtering(img, kernel_size, sigma)
        # if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}_gaussian_sigma.png', gaussian_img/400*255, cmap='gray', vmin=0, vmax=255)
        if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}_gaussian_sigma.png', gaussian_img, cmap='gray', vmin=0, vmax=255)

        binarize_img = (gaussian_img > threshold)*255
        if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}_binarize_mask.png', binarize_img, cmap='gray', vmin=0, vmax=255)


        connect8_img = connect8(binarize_img)
        if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}_8connect_mask.png', connect8_img*255, cmap='gray', vmin=0, vmax=255)
    
        final_img = img*connect8_img + gaussian_img*(connect8_img^True)
        # if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}_final.png', final_img/400*255, cmap='gray', vmin=0, vmax=255)
        # if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}.png', final_img/400*255, cmap='gray', vmin=0, vmax=255)
        # plt.imsave(f'{dirPath}/{Casename}/{Casename}_{i}.png', final_img/400*255, cmap='gray', vmin=0, vmax=255)
        if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}_final.png', final_img, cmap='gray', vmin=0, vmax=255)
        if not only_final: plt.imsave(f'{dirPath}/All/{Casename}/{Casename}_{i}.png', final_img, cmap='gray', vmin=0, vmax=255)
        plt.imsave(f'{dirPath}/{Casename}/{Casename}_{i}.png', final_img, cmap='gray', vmin=0, vmax=255)

        cnt += 1
        if cnt % 10 == 0 : print(cnt)


def FilterAllNii():
    niis = getNiiList(test_nii)
    for nii in niis:
        FilterNii(nii[:-7], only_final)
        


FilterAllNii()



# img_list = getImgList(test_img)
# img_list_by_case = getImgListbyCaseDict(img_list)
# img_order_list_by_case = dict()
# for i in img_list_by_case:
#     img_order_list_by_case[i] = getOrderImgListbyCaseName(i, img_list_by_case[i], back_string)
#     FilterOrderImgList(i, img_order_list_by_case[i], only_final)

