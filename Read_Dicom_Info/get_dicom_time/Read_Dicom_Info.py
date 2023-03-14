import pydicom
import os
import glob
import csv
import datetime
# https://blog.csdn.net/xsz591541060/article/details/108596220?msclkid=d52a4425c78c11ec875945f17d1ff477

SDCT_folder = 'D:\che\Raw_Dicom\Raw_SDCT_Dicom/';
LDCT_folder = 'D:\che\Raw_Dicom\Raw_LDCT_Dicom/';
sub_folder_1 = '\PAT00001\STD00001\SER00001/';
sub_folder_2 = '\PAT00001\STD00001\SER00002/';
file = 'IMG00001'

PatientDict = dict()

def getPatientList(path):
    img_list = glob.glob(path+'*')
    output = [i[len(path):] for i in img_list]
    return output

def setPatientDict(PatientList, folder, state):
    for i in PatientList:
        try:
            dicom = pydicom.read_file(folder + i + sub_folder_1 + file)
            # FL = glob.glob(folder + i + sub_folder_1 + '*')
            StudyDate = dicom.StudyDate
            # print(i)
        except:
            print(i, "err")
            StudyDate = 0
        finally:
            if PatientDict.get(i[:-2], None) == None:
                PatientDict[i[:-2]] = dict()
            PatientDict[i[:-2]][state]= StudyDate[0:4]+"-"+StudyDate[4:6]+"-"+StudyDate[6:]
            # print(type(StudyDate))



setPatientDict(getPatientList(SDCT_folder), SDCT_folder, "SDCT")
setPatientDict(getPatientList(LDCT_folder), LDCT_folder, "LDCT")

for i in PatientDict:
   D_SDCT = PatientDict[i].get("SDCT", "0")
   D_LDCT = PatientDict[i].get("LDCT", "0")
   if D_SDCT != "0" and D_LDCT != "0":
       d = datetime.datetime.strptime(D_SDCT, '%Y-%m-%d')
       d2 = datetime.datetime.strptime(D_LDCT, '%Y-%m-%d')
       delta = d - d2
       PatientDict[i] = [i, D_SDCT, D_LDCT, delta.days]
   else:
       PatientDict[i] = [i, D_SDCT, D_LDCT, "err"]


sortdict = dict(sorted(PatientDict.items(), key=lambda x:-abs(x[1][3]) if x[1][3] != "err" else 1000000))

print('開始寫檔案')
with open('patient_time_sort.csv', 'w', newline='') as patient_height_file:
    writer = csv.writer(patient_height_file)
    writer.writerow(["Patient", "SDCT_StudyDate", "LDCT_StudyDate", "delta"])
    for i in sortdict:
        writer.writerow(sortdict[i])

