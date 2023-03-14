from distutils.log import error
from msilib.schema import Error

fname = r'D:\CAC_project\mark_score_compare\Score_v1.0_1sum.csv'  # SDCT score


import pandas as pd
import csv
from src.dir_tool import *
from cal_agastone import *

#####################################################################################
'''
NiiDataPath == LDCT tranfer to LDCT* nii folder
MarkDataPat == mark Floder Path
'''
# NiiDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii_old\label/'
MarkDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\result\total288/'
NiiDataPath = r'D:\CAC_project\png2nii\datasets\Create-Nii\label\total288/'
csv_filename = 'output.csv'
isHuMap = True
score_step = [130, 139, 240, 400]

isExec_odds_timeError = False
######################################################################################
odds = ['14880321', '10982384', '16291433', '14692672', '15277153', '14913714', '13418490', '15932588', '12782477', '15952315', '16385447', '14153174', '16593230', '16176026', '16198768', '12439973', '16034187', '15564984', '15646114', '10982384', '11151136', '11756186', '12064505', '12164066', '12782477', '14913714', '14927345', '14961569', '15124444', '16385210', '16169361', '16194517', '16386882', '16480389', '16796751']

time_err = ['8106669', '14880321', '1443374', '14133892', '2185695', '13607335', '11630016', '15181290', '13608032', '4971317', '14718457', '8113244', '4388287', '3022342', '16198768', '12439973', '13811444', '1443556','1476024','1523688','778494','8790850','16550462','17241406','17318295','9529968']

dict_from_csv = pd.read_csv(fname, header=None, index_col=0, squeeze=True, encoding='ISO-8859-1').to_dict()

with open(csv_filename, 'w', newline='', encoding='ISO-8859-1') as patient_height_file:
    pass
all_case = get_all_case_by_sub_dirs(get_all_sub_dirs(MarkDataPath))
# all_case = ['15952315-M','13418490-M','15932588-L','12782477-L','16385447-L']

LDCTtoSDCT_dict = dict()
for i in all_case:
    if i in dict_from_csv[1].keys():
        LDCTtoSDCT_dict[i] = i
    elif i[:-2]+"-P" in dict_from_csv[1].keys():
        LDCTtoSDCT_dict[i] = i[:-2]+"-P"
    elif i[:-2]+"-G" in dict_from_csv[1].keys():
        LDCTtoSDCT_dict[i] = i[:-2]+"-G"
    else:
        LDCTtoSDCT_dict[i] = "Error"

def isOKcase(casename):
    if LDCTtoSDCT_dict[casename] == "Error":
        print(casename, '沒有對應SDCT 檔案')
        return False
    if not isExec_odds_timeError:
        if casename[:-2] in odds:
            print(casename, '檔案資料怪怪的')
            return False
        elif casename[:-2] in time_err:
            print(casename, '檔案資料時間相差太大')
            return False
    return True


all_case = list(filter(isOKcase, all_case))

# print(all_case)

Data_Dict = dict()
x_SDCT_score = []
y_LDCT_score = []
SDCT_Class = {
    "No" : {"Number" : 0, "No": 0, "Low": 0, "Middle" : 0, "High" : 0, "Higher" : 0, "Error" :0},
    "Low" : {"Number" : 0, "No": 0, "Low": 0, "Middle" : 0, "High" : 0, "Higher" : 0, "Error" :0},
    "Middle" : {"Number" : 0, "No": 0, "Low": 0, "Middle" : 0, "High" : 0, "Higher" : 0, "Error" :0},
    "High" : {"Number" : 0, "No": 0, "Low": 0, "Middle" : 0, "High" : 0, "Higher" : 0, "Error" :0}, 
    "Higher" : {"Number" : 0, "No": 0, "Low": 0, "Middle" : 0, "High" : 0, "Higher" : 0, "Error" :0}, 
    "Error" : {"Number" : 0, "No": 0, "Low": 0, "Middle" : 0, "High" : 0, "Higher" : 0, "Error" :0}
}

if isHuMap:
    print('開啟Hu 對應計算分數', score_step) 

for i in all_case:
    if LDCTtoSDCT_dict[i] == "Error":
        Data_Dict[i] = [i, "Error", "Error", "Error", "Error", "" , "Error", "Error", "Error"]

    else:
        try:
            temp_score = caculat_agatstone(NiiDataPath, MarkDataPath, i, score_step = (score_step if isHuMap else [130, 200, 300, 400, float ('inf') ]))
            # print(temp_score)
            agastone = int(temp_score)
            x_SDCT_score.append(dict_from_csv[1][LDCTtoSDCT_dict[i]])
            y_LDCT_score.append(agastone)
        except Exception as e:
            agastone = "Error"
            print(i, '發生錯誤:' , e)

            
        # agastone = int(caculat_agatstone(NiiDataPath, MarkDataPath, i))
        # x_SDCT_score.append(dict_from_csv[1][LDCTtoSDCT_dict[i]])
        # y_LDCT_score.append(agastone)
        Data_Dict[i] = [LDCTtoSDCT_dict[i], i, dict_from_csv[1][LDCTtoSDCT_dict[i]], agastone]
        if Data_Dict[i][2] == 0:
            Data_Dict[i].append(0)
        elif Data_Dict[i][3] == "Error":
            Data_Dict[i].append("Error")
        else:
            Data_Dict[i].append(abs(Data_Dict[i][3]-Data_Dict[i][2])/Data_Dict[i][2])

        Data_Dict[i] += ["", agastone_class(Data_Dict[i][2]), agastone_class(Data_Dict[i][3])]

        if Data_Dict[i][-1] == Data_Dict[i][-2]:
            Data_Dict[i].append("True")
        else:
            Data_Dict[i].append("False")
    
        SDCT_Class[Data_Dict[i][-3]]["Number"] += 1
        try:
            SDCT_Class[Data_Dict[i][-3]][Data_Dict[i][-2]] += 1
        except Exception as e:
                print(i, '發生錯誤:' , e)


# for x in Data_Dict:
#     print(Data_Dict[x][2],Data_Dict[x][3])
all_case = sorted(all_case, key=lambda x: 1 if type(Data_Dict[x][2]) == str or type(Data_Dict[x][3]) == str else -(Data_Dict[x][2]*Data_Dict[x][3]))
# print([type(Data_Dict[x][2]) for x in all_case])



print('開始寫檔案')
with open(csv_filename, 'w', newline='', encoding='ISO-8859-1') as patient_height_file:
    writer = csv.writer(patient_height_file)
    writer.writerow(["SDCT_File", "LDCT_File", "Origin_Score", "Predict_Score", "Pedict_error", "","Origin_class", "Predict_class", "isSameClass"])
    for i in all_case:
        writer.writerow(Data_Dict[i])

def plt_score_compare(dat, line, filename):
    df = pd.DataFrame(dat)
    import seaborn as sb
    from matplotlib import pyplot as plt
    sb.lmplot(x='SDCT_score',y='LDCT_score', data = df)
    plt.grid()
    plt.plot([0, line], [0, line], color="red")
    plt.savefig(filename)

print(x_SDCT_score)
print(y_LDCT_score)
plt_score_compare({'SDCT_score':x_SDCT_score,'LDCT_score':y_LDCT_score}, 1500, "score_compare.png")
plt_score_compare({'SDCT_score':np.clip(np.array(x_SDCT_score), 0 , 1000),'LDCT_score':np.clip(np.array(y_LDCT_score), 0 , 1000)}, 1000, "score_compare_unforcus1000.png")

col=["S_No", "S_Low", "S_Middle", "S_High", "S_Higher", "S_Error"]
row=["number", "L_No", "L_Low", "L_Middle", "L_High", "L_Higher", "L_Error"]
# print(dict2Array2D(SDCT_Class))
vals = np.around(dict2Array2D(SDCT_Class), decimals=3).T
# #行名

plt.figure(figsize=(20,8))
tab = plt.table(cellText=vals, 
              colLabels=col, 
             rowLabels=row,
              loc='center', 
              cellLoc='center',
              rowLoc='center')
tab.scale(0.7,3)
tab.auto_set_font_size(False)
tab.set_fontsize(30)
plt.axis('off')
plt.savefig("class_diff.png")



