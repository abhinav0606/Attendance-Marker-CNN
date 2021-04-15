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
else:
    status="Data doesnt matched"
print("Present")
date=str(datetime.datetime.now()).split(" ")[0]
excell_sheet=pd.read_excel("Attendance.xlsx")
columns=excell_sheet.columns
if columns==[]:
    pass
else:
    for i in columns:
        if "Unnamed" in i:
            excell_sheet.drop(i,axis=1,inplace=True)
        else:
            pass
