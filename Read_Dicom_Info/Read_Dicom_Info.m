%% Read Dicom Info

% file path
folder = 'D:\che\Raw_Dicom\Raw_SDCT_Dicom\';
% name = '133993-G';
file = '\PAT00001\STD00001\SER00001\IMG00001';

namelist = dir([folder,'*.DICOM']); %提取DICOM檔案的檔案資訊
l =length(namelist); %DICOM檔案的個數

for i = 1:l
fullname = [folder,namelist(i).name]; %儲存路徑+檔名=絕對路徑
% a = importdata(fullname); %將檔案中的資料賦值到矩陣中
path = [folder, fullname, file];

info = dicominfo(path);
patient_height = info.PatientSize;
fprintf('patient_height = %.2f',patient_height)
end

% path = [folder, fullname, file];
% info = dicominfo(path);

% A = dir(fullfile('D:\che\Raw_Dicom\Raw_SDCT_Dicom\','*.txt'));

% %Pixel Spacing
% Pixel_Spacing = info.PixelSpacing;
% Slice_Spacing = info.SpacingBetweenSlices;
%fprintf('Pixel spacing = %d, %d, %d/n', Pixel_Spacing(1), Pixel_Spacing(2), Slice_Spacing);

% 身高
% patient_height = info.PatientSize;
% fprintf('patient_height = %.2f',patient_height)
