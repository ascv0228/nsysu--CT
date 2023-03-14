
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
import json 
from src.nii2png import *
      
case = '11151136'

path_dict = {
    'LDCT':{
        'MarkDataPath': r'D:/CAC_project/png2nii/datasets/Create-Nii/label/result/total250/',
        'NiiDataPath': r'D:/CAC_project/png2nii/datasets/Create-Nii/label/total150/'},
    'SDCT':{
        'MarkDataPath': r'D:/CT_file/CT_label/',
        'NiiDataPath': r'D:/che/LDCT/BM3D/SDCT_nii_forBM3D/'},
        }

time_err = ['8106669', '14880321', '1443374', '14133892', '2185695', '13607335', '11630016', '15181290', '13608032', '4971317', '14718457', '8113244', '4388287', '3022342', '16198768', '12439973', '13811444', '1443556','1476024','1523688','778494','8790850','16550462','17241406','17318295','9529968']
def get_area(NiiDataPath,  case_name, PredictLabelPath):
    global run
    datapath = NiiDataPath + case_name + '.nii.gz'  # 改檔名
    if (not os.path.isfile(datapath)):
        return {
            'start_z': 'FileNotFoundError',
            'PixelSpacing_x': 'FileNotFoundError', 
            'PixelSpacing_y': 'FileNotFoundError', 
            'PixelSpacing_z': 'FileNotFoundError', 
            'GuessPixelSpacing_z': 'FileNotFoundError', 
            'area': 'FileNotFoundError', 
            'slice_data': 'FileNotFoundError'
            }
    img = nib.load(datapath)
    img_arr = img.get_fdata()  # 取得影像陣列
    hdr = img.header.copy()  # 取得nii檔頭
    area = 0
    HuValues = dict()
    try:
        slice_thickness = round(hdr['srow_z'][2], 1)
        if slice_thickness < 1.5:
            slice_thickness = 2.0
    except:
        slice_thickness = 2.5
    # find pixel spacing
    PixelSpacing_x = hdr['pixdim'][1]  # 或  nii.header.get_zooms()
    PixelSpacing_y = hdr['pixdim'][2]  # 或  nii.header.get_zooms()
    PixelSpacing_z = hdr['pixdim'][3]
    # print('x', PixelSpacing_x)
    # print('y', PixelSpacing_y)
    # print('z', PixelSpacing_z)
    # print('z', slice_thickness)
    start_mm = hdr['srow_z'][3]
    sub_areas = dict()
    # if PixelSpacing_x > 0.488282 or PixelSpacing_x < 0.488280:
    #     print(f'File : {case_name} ,  PixelSpacing = {PixelSpacing_x}')

    # read label information
    # PredictLabelPath = getMarkDataPathbyCase(MarkDataPath, case_name) + '1.nii.gz'
    for p_path in PredictLabelPath:
        imgLabel = nib.load(p_path)
        img_arrLabel = imgLabel.get_fdata()

        for slice in range(img_arrLabel.shape[2]):
            # print((img_arrLabel[:, :, slice] != 1))
            Class1 = np.where(img_arrLabel[:, :, slice] == 1)  # 1為鈣化區  Class1為鈣化區的x,y座標
            # print(Class1)
            imgShape = np.shape(img_arrLabel)
            Class1Image = np.zeros((imgShape[0], imgShape[1]))
            Class1Image[img_arrLabel[:, :, slice] != 1] = 0
            Class1Image[img_arrLabel[:, :, slice] == 1] = 1
            Class1Image[img_arrLabel[:, :, slice] == 2] = 1
            Class1Image[img_arrLabel[:, :, slice] == 3] = 1

            if Class1[0].any() == True:  # any() : 如果都为空、0、false，则返回false(無發現鈣化)，如果不都为空、0、false，则返回true(有鈣化)。
                Class1 = list(Class1)

                a = measure.label(Class1Image, connectivity=2)  # 對於二維來說，當connectivity=1時代表4連通，當connectivity=2時代表8連通

                # plt.imshow(a*255)
                # plt.show()
                sub_dict = dict()
                sub_area = 0
                for connect8 in range(1, a.max() + 1):  # a.max() >> 計算標註的label區塊數量
                    HuValue = 0
                    countPixel = 0
                    connect8Pixel = np.where(a == connect8)  # connect8Pixel = 鈣化pixel位置

                    for xAxis, yAxis in zip(connect8Pixel[0], connect8Pixel[1]):
                        Curr_HuValue = img_arr[xAxis, yAxis, slice]  # 依序取得每一個鈣化pixel的Hu值

                        if HuValue < Curr_HuValue:  # 保留最大Hu值
                            HuValue = Curr_HuValue
                        if Curr_HuValue >= 130:  # 避免"預測為鈣化,但Hu值卻小於130"
                            countPixel = countPixel + 1

                    if HuValue < 130: # 130
                        sub_a = 0
                    else:
                        sub_a = countPixel * PixelSpacing_x * PixelSpacing_y * (PixelSpacing_z / 3)
                    
                    sub_area += sub_a
                    sub_dict[connect8] = {'area' :sub_a, 'HU': 0 if HuValue < 130 else HuValue}
                sub_areas[f'slice = {slice}'] = {'actual_z':f'{start_mm + slice * PixelSpacing_z} mm', 
                                                    'total_area': sub_area,'detail':sub_dict}
                area += sub_area

    return {
            'start_z': hdr['srow_z'][3],
            'PixelSpacing_x': PixelSpacing_x, 
            'PixelSpacing_y': PixelSpacing_y, 
            'PixelSpacing_z': PixelSpacing_z, 
            'GuessPixelSpacing_z': slice_thickness, 
            'area': round(area, 3), 
            'slice_data': sub_areas
            }


def PredictLabelPath(ct_type, case_name):
    if ct_type == 'LDCT':
        return [path_dict[ct_type]['MarkDataPath']  + case_name + r'.nii_0_0_1/RoiVolume/'+ '1.nii.gz']
    elif ct_type == 'SDCT':
        return filter(os.path.isfile,[ path_dict[ct_type]['MarkDataPath'] + case_name + f'/RoiVolume/{i}.nii.gz' for i in range(1,4)])

def  i_need_filename(ct_type, s):
    if ct_type == 'SDCT':
        P = ['10831273', '10831740', '10847139', '10946711', '10982384', '10991181', '11063017', '11149590', '11151136', '11203637', '11266276', '11273839', '11293155', '11325669', '11418829', '11426463', '11514902', 
            '11560604', '11618114', '11756186', '11851493', '11903790', '12064118', '12069908', '12273426', '12331509', '12349450', '12349529', '12372519', '12373205', '12382820', '12400474', '12477677', '12560600',
            '12749007', '12782477', '12788475', '12837477', '12862634', '12933196', '12966108', '12967485', '13089173', '13239844', '13243204', '13326493', '13395396', '13607926', '13608361', '13734479', '13837837', 
            '13838556', '13947916', '13959143', '14087548', '14133892', '14152579', '14165663', '14168935', '14271148', '14631686', '14689895', '14692672', '14791845', '14888358', '14913714', '14961569', '14966984', 
            '14970537', '14985467', '14985650', '15132180', '15197827', '15198615', '15226354', '15326939', '15646114', '15702666', '15798251', '15842952', '15932588', '15956044', '15960562', '16059828', '16059975', 
            '16061511', '16071184', '16091386', '16155310', '16169361', '16176026', '16176037', '16176673', '16184035', '16185276', '16185710', '16194517', '16198144', '16198826', '16221480', '16254641', '16291080', 
            '16291604', '16291784', '16292538', '16294705', '16320777', '16358988', '16379763', '16383225', '16383861', '16385390', '16385425', '16385447', '16386257', '16411668', '16477513', '16477864', '16480232',
            '16480389', '16480583', '16480685', '16480856', '16503756', '16544528', '16593230', '16796751', '16822223', '16822665', '16822892', '16835511', '16855304', '16855553', '16855962', '16855995', '16860030', 
            '16860267', '16860518', '16860734', '16927336', '16932006', '16932313', '16932437', '16932448', '16932459']
        G = ['10824905', '10935350', '10997930', '11028685', '11078618', '11272029', '11318608', '11326480', '11338286', '11369645', '11427580', '11458698', '11610449', '11653002', '11934240', '12064505', '12064743', '12069339', '12071055', '12164066', '12164511', '12254089', '12255253', '12264094', '12284581', '12383130', '12439973', '12460707', '12587767', '12625660', '12656109', '12788964', 
            '12820256', '12838889', '12894596', '12930879', '12930915', '12932411', '12939570', '12942380', '13090396', '13159790', '13167629', '13222689', '13245404', '13285262', '13289797', '13289899', '13300486', '13321545', '13395192', '13418490', '13459079', '13479168', '13481511', '13552120', '13552562', '13563047', '13603786', '13604290', '13607493', '13608769', '13615468', '13736282', '13760833', '13886969', '13992819', '14019068', '14046481', '14104484', '14153174', '14165436', '14166406', '14168184', '14173638', '14254252', '14316564', '14596588', '14668521', '14675457', '14718457', '14800034', '14803237', '14808243', '14818474', '14818894', '14851208', '14880321', '14880343', '14888290', '14927345', '15064627', '15124444', '15277153', '15305632', '15319149', '15336239', '15375709', '15404098', '15404678', '15455524', '15512591', '15539589', '15549356', '15553512', '15564984', '15581234', '15648621', '15750831', 
            '15753078', '15755109', '15762295', '15842612', '15862381', '15867239', '15868710', '15945343', '15951709', '15952315', '15998444', '16028696', '16034187', '16049471', '16059157', '16059657', '16059771', '16071015', '16074376', '16096881', '16170459', '16176479', '16194788', '16194915', '16198177', '16198393', '16198768', '16285339', '16291422', '16291433', '16300268', '16383281', '16383510', '16385210', '16386882', '16468625', '16470658', '16472734', '16480903', '16508831', '16654378', '16704920', '16797947', '16822110', '16932211', '16949078']
        if(s in P ): return s + '-P'
        if(s in G ): return s + '-G'
    elif ct_type == 'LDCT':
        L = ['10831273', '10831740', '10847139', '10946711', '10982384', '10991181', '11063017', '11149590', '11151136', '11203637', '11266276', '11273839', '11293155', '11325669', '11418829', '11426463', '11514902', '11560604', '11618114', '11756186', '11851493', '11903790', '12064118', '12069908', '12273426', '12331509', '12349450', '12349529', '12372519', '12373205', '12382820', '12400474', '12477677', '12560600', '12749007', '12782477', '12788475', '12837477', '12862634', '12933196', '12966108', '12967485', '13089173', '13239844', '13243204', '13326493', '13395396', '13607926', '13608361', '13734479', '13837837', '13838556', '13947916', '13959143', '14087548', '14133892', '14152579', '14165663', '14168935', '14271148', '14631686', '14689895', '14692672', '14791845', '14888358', '14913714', '14961569', '14966984', '14970537', '14985467', '14985650', '15132180', '15197827', '15198615', '15226354', '15326939', '15646114', '15702666', '15798251', '15842952', '15932588', '15956044', '15960562', '16059828', '16059975', '16061511', '16071184', '16091386', '16155310', '16169361', '16176026', '16176037', '16176673', '16184035', '16185276', '16185710', '16194517', '16198144', '16198826', '16221480', '16254641', '16291080', '16291604', '16291784', '16292538', '16294705', '16320777', '16358988', '16379763', '16383225', '16383861', '16385390', '16385425', '16385447', '16386257', '16411668', '16477513', '16477864', '16480232', '16480389', '16480583', '16480685', '16480856', '16503756', '16544528', '16593230', '16796751', '16822223', '16822665', '16822892', '16835511', '16855304', '16855553', '16855962', '16855995', '16860030', '16860267', '16860518', '16860734', '16927336', '16932006', '16932313', '16932437', '16932448', '16932459']
        M = ['10824905', '10935350', '10997930', '11028685', '11078618', '11272029', '11318608', '11326480', '11338286', '11369645', '11427580', '11458698', '11610449', '11653002', '11934240', '12064505', '12064743', '12069339', '12071055', '12164066', '12164511', '12254089', '12255253', '12264094', '12284581', '12383130', '12439973', '12460707', '12587767', '12625660', '12656109', '12788964', '12820256', '12838889', '12894596', '12930879', '12930915', '12932411', '12939570', '12942380', '13090396', '13159790', '13167629', '13222689', '13245404', '13285262', '13289797', '13289899', '13300486', '13321545', '13395192', '13418490', '13459079', '13479168', '13481511', '13552120', '13552562', '13563047', '13603786', '13604290', '13607493', '13608769', '13615468', '13736282', '13760833', '13886969', '13992819', '14019068', '14046481', '14104484', '14153174', '14165436', '14166406', '14168184', '14173638', '14254252', '14316564', '14596588', '14668521', '14675457', '14718457', '14800034', '14803237', '14808243', '14818474', '14818894', '14851208', '14880321', '14880343', '14888290', '14927345', '15064627', '15124444', '15277153', '15305632', '15319149', '15336239', '15375709', '15404098', '15404678', '15455524', '15512591', '15539589', '15549356', '15553512', '15564984', '15581234', '15648621', '15750831', '15753078', '15755109', '15762295', '15842612', '15862381', '15867239', '15868710', '15945343', '15951709', '15952315', '15998444', '16028696', '16034187', '16049471', '16059157', '16059657', '16059771', '16071015', '16074376', '16096881', '16170459', '16176479', '16194788', '16194915', '16198177', '16198393', '16198768', '16285339', '16291422', '16291433', '16300268', '16383281', '16383510', '16385210', '16386882', '16468625', '16470658', '16472734', '16480903', '16508831', '16654378', '16704920', '16797947', '16822110', '16932211', '16949078']
        if(s in L ): return s + '-L'
        if(s in M ): return s + '-M'
    return s

def get_area2(case):
    print(case)
    d = dict()
    if case in time_err:
        print(case, 'SDCT和LDCT日期相差太多')
        d['LDCT']['time-error'] = True
        d['SDCT']['time-error'] = True
    for ct_type in ['LDCT', 'SDCT']:
        d[ct_type] = get_area(path_dict[ct_type]['NiiDataPath'], i_need_filename(ct_type, case), PredictLabelPath(ct_type, i_need_filename(ct_type, case)))

    return d

basePath = f'detail/{case}'
if os.path.exists(basePath):
    shutil.rmtree(basePath)
os.makedirs(basePath)
os.makedirs(basePath + '/LDCT')
os.makedirs(basePath + '/SDCT')

case_txt = open(f'{basePath}/{case}.txt', 'w')
data = get_area2(case)
# print(data['LDCT'].keys())
l_f = i_need_filename( 'LDCT', case )
s_f = i_need_filename( 'SDCT', case )
print(f"case: {case}" , file= case_txt)
print(f"LDCT_casename: {l_f}" , file= case_txt)
print(f"SDCT_casename: {s_f}" , file= case_txt)
print(f"LDCT_origin_file: {path_dict['LDCT']['NiiDataPath']+ l_f + '.nii.gz'}" , file= case_txt)
print(f"LDCT_marked_file: {PredictLabelPath('LDCT', l_f)}" , file= case_txt)
print(f"SDCT_origin_file: {path_dict['SDCT']['NiiDataPath']+ s_f + '.nii.gz'}" , file= case_txt)
s_mark_file = ',\n'.join(PredictLabelPath('SDCT', s_f))
print(f"SDCT_marked_file: {s_mark_file}" , file= case_txt)
print(f"\n" , file= case_txt)
if 'time-error' in data['LDCT']:
    print(f"警告: SDCT和LDCT日期相差太多" , file= case_txt)
    print(f"警告: SDCT和LDCT日期相差太多" , file= case_txt)
    print(f"警告: SDCT和LDCT日期相差太多" , file= case_txt)
    print(f"\n" , file= case_txt)
print(f"LDCT_area: {data['LDCT']['area']}" , file= case_txt)
print(f"SDCT_area: {data['SDCT']['area']}" , file= case_txt)
print(f"\n" , file= case_txt)
for ct_type in ['LDCT', 'SDCT']:
    print(f"==========================={ct_type}===========================" , file= case_txt)
    if 'time-error' in data[ct_type]:
        print(f"警告: SDCT和LDCT日期相差太多" , file= case_txt)
        print(f"警告: SDCT和LDCT日期相差太多" , file= case_txt)
        print(f"警告: SDCT和LDCT日期相差太多" , file= case_txt)
    print(f"start_z: {data[ct_type]['start_z']}" , file= case_txt)
    print(f"actual_x: {data[ct_type]['PixelSpacing_x']}" , file= case_txt)
    print(f"actual_y: {data[ct_type]['PixelSpacing_y']}" , file= case_txt)
    print(f"actual_z: {data[ct_type]['PixelSpacing_z']}" , file= case_txt)
    print(f"guess_z: {data[ct_type]['GuessPixelSpacing_z']}" , file= case_txt)
    print(f"start_z: {data[ct_type]['start_z']}" , file= case_txt)
    json_object = json.dumps(data[ct_type]['slice_data'], indent = 4) 
    print(f"slice_data: {json_object}" , file= case_txt)

nii2png_dict = {
    'LDCT' :{
        'case_name' : l_f,
        'origin_file': path_dict['LDCT']['NiiDataPath']+ l_f + '.nii.gz',
        'storage_location': basePath + '/LDCT/'
    },
    'SDCT' :{
        'case_name' : s_f,
        'origin_file': path_dict['SDCT']['NiiDataPath']+ s_f + '.nii.gz',
        'storage_location': basePath + '/SDCT/'
    }
}
for i in nii2png_dict:
    nii_to_png(nii2png_dict[i]['origin_file'], nii2png_dict[i]['storage_location'], nii2png_dict[i]['case_name'])
case_txt.close()
