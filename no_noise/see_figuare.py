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

path = r'D:\CAC_project\no_noise\result2/'
filename = '11426463-L_58.png'
# filename = '11151136-L_27.png'

img = np.array(Image.open(path + filename))
plt.imshow(img, cmap='gray', vmin = 0, vmax = 255)
plt.show()
