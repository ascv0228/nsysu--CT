import pydicom
import os
import glob
import csv
# https://blog.csdn.net/xsz591541060/article/details/108596220?msclkid=d52a4425c78c11ec875945f17d1ff477

folder = 'D:\che\Raw_Dicom\Raw_SDCT_Dicom/';
sub_folder_1 = '\PAT00001\STD00001\SER00001/';
sub_folder_2 = '\PAT00001\STD00001\SER00002/';
file = 'IMG00001'

def getPatientList(path):
    img_list = glob.glob(path+'*')
    output = [i[len(path):] for i in img_list]
    return output

PatientList = getPatientList(folder)

PatientDict = dict()
for i in PatientList:
    try:
        dicom = pydicom.read_file(folder + i + sub_folder_1 + file)
        FL = glob.glob(folder + i + sub_folder_1+'*')
        Len = len(FL)
        Err = ' '
        if Len == 3:
            Len = len(glob.glob(folder + i + sub_folder_2+'*'))
            Err = 'True'
        Height = dicom.PatientSize
    except:
        Height = 0
    finally:
        PatientDict[i] = [Height, Len, Err]


sortdict = dict(sorted(PatientDict.items(), key=lambda x:-x[1][0]))
print('開始寫檔案')
with open('patient_height_imgNum.csv', 'w', newline='') as patient_height_file:
    writer = csv.writer(patient_height_file)
    writer.writerow(["Patient", "Height", "imgNum", "SER00001-3Imgs"])
    for i in sortdict:
        try:
            writer.writerow([i, sortdict[i][0], sortdict[i][1], sortdict[i][2]])
        except:
            continue
