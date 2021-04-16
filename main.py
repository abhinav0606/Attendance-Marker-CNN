import os
import cv2
import numpy as np
import pandas as pd
import datetime
import xlsxwriter,xlrd
from tensorflow.keras.models import load_model
student_name=input("Enter the Student name")
student_id=input("Enter the Student Id")
student_name=student_name.replace(" ","_").lower()
student_id=student_id.lower()
folder=student_id+"_"+student_name
student_data=os.listdir("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Train")
if folder in student_data:
    pass
else:
    print("No data of this Student")
    exit()
model=load_model("CNN_ATTENDENCE.h5")
capture=cv2.VideoCapture(0)
faces=cv2.CascadeClassifier("frontal_face.xml")
l=[]
while True:
    ret,frame=capture.read()
    frame=cv2.flip(frame,1)
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=faces.detectMultiScale(gray_frame,1.3,5)
    for (x,y,w,h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),thickness=3)
        cv2.imshow("Frame",frame)
        crop_frame=gray_frame[y:y+h,x:x+w]
        new_size=np.expand_dims(np.expand_dims(cv2.resize(crop_frame,(48,48)),-1),0)
        prediction=model.predict(new_size)
        index=int(np.argmax(prediction))
        l.append(index)
    if cv2.waitKey(1)==13 or len(l)==150:
        break
capture.release()
cv2.destroyAllWindows()
dict={}
for i in l:
    dict[i]=l.count(i)
dict=max(dict,key=lambda x:x)
index=student_data[dict]
status=""
if index==folder:
    status="Present"
    print("Present")
else:
    status="Data doesnt matched"
    print("Data doesnt matched")
date=str(datetime.datetime.now()).split(" ")[0]
workbook_read=xlrd.open_workbook("Attendance.xlsx")
sheet=workbook_read.sheet_by_index(0)
workbook_write=xlsxwriter.Workbook("Attendance.xlsx")
worksheet_write=workbook_write.add_worksheet()
bold = workbook_write.add_format({'bold': True})
heading_section=[]
for i in range(sheet.ncols):
    heading_section.append(sheet.cell(0,i).value)
for i in range(sheet.ncols):
    worksheet_write.write(0,i,sheet.col(i)[0].value,bold)
    for j in range(1,len(sheet.col(i))):
        worksheet_write.write(j,i,sheet.col(i)[j].value)
if date not in heading_section:
    worksheet_write.write(0,sheet.ncols,date,bold)
    worksheet_write.write(1,sheet.ncols,student_id)
else:
    index=heading_section.index(date)
    worksheet_write.write(len(sheet.col(index)),index,student_id)
workbook_write.close()