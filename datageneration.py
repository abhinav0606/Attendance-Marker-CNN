import cv2
import numpy
import os
student_name=input("Enter the Name of the student")
student_id=input("Enter the ID of the student")
student_name=student_name.replace(" ","_").lower()
student_id=student_id.lower()
folder=student_id+"_"+student_name
try:
    os.mkdir("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Test/"+folder)
    os.mkdir("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Train/"+folder)
except:
    print("Already Existed")
    exit()
video=cv2.VideoCapture(0)
haarcascade=cv2.CascadeClassifier("frontal_face.xml")
count=0
while True:
    ret,frame=video.read()
    frame=cv2.flip(frame,1)
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    har_face=haarcascade.detectMultiScale(gray_frame,1.3,5)
    for (x,y,w,h) in har_face:
        cropped=frame[y:y+h,x:x+w]
        cv2.imshow("Cropped",cropped)
        if count<=400:
            cv2.imwrite("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Train/"+folder+"/"+str(count)+".jpg",cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY))
            count=count+1
        else:
            cv2.imwrite("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Test/"+folder+"/"+str(count)+".jpg",cv2.cvtColor(frame[y:y+h,x:x+w],cv2.COLOR_BGR2GRAY))
            count=count+1
    if cv2.waitKey(1)==13 or count==500:
        break
video.release()
cv2.destroyAllWindows()