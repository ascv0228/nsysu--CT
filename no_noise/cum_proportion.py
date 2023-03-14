from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import skimage.io as io
import pandas as pd
import os
import glob
import shutil


case = '10982384'


# base_case =  r'D:\CAC_project\crop_hearts\data/'
# read_LDCT_path = base_case + 'read/' + case +'\LDCT/'
read_LDCT_path = r'D:\CAC_project\cut\Raw_LDCT_PNG6\10982384-L/'
# read_SDCT_path = base_case + 'read/' + case +'\SDCT/'
output_LDCT_path = r'D:\CAC_project\no_noise\test_img_2/origin_LDCT/'
# output_LDCT_path = base_case + 'output/' + case +'\LDCT/'
# output_SDCT_path = base_case + 'output/' + case +'\SDCT/'

# paths = [read_LDCT_path, read_SDCT_path, output_LDCT_path, output_SDCT_path]
paths = [read_LDCT_path,output_LDCT_path]
# if not os.path.exists(read_LDCT_path):
#     print('Need path :', read_LDCT_path)
#     exit(1)
# if not os.path.exists(read_SDCT_path):
#     print('Need path :', read_SDCT_path)
#     exit(1)

for i in paths:
    if not os.path.exists(i):
        os.makedirs(i)

all_D = dict()
all_D[paths[0]] = dict()
all_D[paths[1]] = dict()

def getImgList(path):
    img_list = glob.glob(path + '/*.png')
    output = [i[len(path):] for i in img_list]
    return output
def adds(d1, d2):
    return {key: d1.get(key, 0) + d2.get(key, 0)
          for key in set(d1) | set(d2)}

def get_keys_values_cum(d):
    keys = list(sorted(d.keys()))
    values = [d[i] for i in keys]
    cumulative = np.cumsum(values)/np.sum(values)
    return keys, values, cumulative

def divs(d, num):
    return {key: d.get(key, 0)/num for key in d}

def output_cum(read_path, output_path):
    for i in getImgList(read_path):
        ar=np.array(Image.open(read_path + i).convert('L'), 'f')
        print('img',np.sum(ar > 253))
        ar_unique, count = np.unique(ar, return_counts=True)
        temp_dict = dict(zip(ar_unique, count))
        all_D[read_path] = adds(all_D[read_path], temp_dict)
        cumulative = np.cumsum( count)/np.sum(count)
        plt.clf()
        plt.plot( ar_unique,cumulative,  c='blue')
        plt.grid()
        plt.savefig(output_path+i)
    else:
        keys = list(sorted(all_D[read_path].keys()))
        values = [all_D[read_path][i] for i in keys]
        cumulative = np.cumsum(values)/np.sum(values)
        
        plt.clf()
        plt.plot( keys,cumulative,  c='blue')
        plt.grid()
        plt.savefig(output_path+'all.png')

# def print_all_LDCT_SDCT():
#     keys_L, values_L, cum_L = get_keys_values_cum(all_D[paths[0]])
#     keys_S, values_S, cum_S = get_keys_values_cum(all_D[paths[1]])
            
#     plt.clf()
#     plt.plot( keys_L, cum_L,  c='blue')
#     plt.grid()
#     plt.savefig(base_case + 'output/' + case +'/LDCT_all.png')
#     plt.clf()
#     plt.plot( keys_S, cum_S,  c='blue')
#     plt.grid()
#     plt.savefig(base_case + 'output/' + case +'/SDCT_all.png')
#     plt.clf()
#     plt.plot( keys_S, cum_S,  c='blue')
#     plt.plot( keys_L, cum_L,  c='green')
#     plt.grid()
#     plt.savefig(base_case + 'output/' + case +'/all.png')

output_cum(read_LDCT_path, output_LDCT_path)
# output_cum(read_SDCT_path, output_SDCT_path)
# print_all_LDCT_SDCT()