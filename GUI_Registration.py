from tkinter import *
import cv2
import os
def login():
    student_name=name.get()
    student_id=id.get()
    student_id=student_id.lower()
    student_name=student_name.lower()
    student_name=student_name.replace(" ","_")
    folder_name=student_id+"_"+student_name
    try:
        os.mkdir("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Test/"+folder_name)
        os.mkdir("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Train/"+folder_name)
    except:
        exit()
    video = cv2.VideoCapture(0)
    haarcascade = cv2.CascadeClassifier("frontal_face.xml")
    count = 0
    while True:
        ret, frame = video.read()
        frame = cv2.flip(frame, 1)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        har_face = haarcascade.detectMultiScale(gray_frame, 1.3, 5)
        for (x, y, w, h) in har_face:
            cropped = frame[y:y + h, x:x + w]
            cv2.imshow("Cropped", cropped)
            if count <= 400:
                cv2.imwrite("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Train/" + folder_name + "/" + str(
                    count) + ".jpg", cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY))
                count = count + 1
            else:
                cv2.imwrite("/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Test/" + folder_name + "/" + str(
                    count) + ".jpg", cv2.cvtColor(frame[y:y + h, x:x + w], cv2.COLOR_BGR2GRAY))
                count = count + 1
        if cv2.waitKey(1) == 13 or count == 500:
            name.set("")
            id.set("")
            break
    video.release()
    cv2.destroyAllWindows()

root=Tk()
root.geometry("500x500")
name=StringVar()
id=StringVar()
root.title("Registration Panel")
Label(root,text="Registration Panel",font="arial 16 bold").pack(side=TOP)
Label(root,text="Abhinav Gangrade\nSDE-Dell Technologies",font="arial 16 bold").pack(side=BOTTOM)
Label(root,text="Enter the Name:",font="arial 13 bold").place(x=70,y=120)
Entry(root,textvariable=name,bg="ghost white").place(x=220,y=120)
Label(root,text="Enter the Id:",font="arial 13 bold").place(x=70,y=200)
Entry(root,textvariable=id,bg="ghost white").place(x=220,y=200)
Button(root,text="Register",font="arial 13 bold",command=login).place(x=180,y=280)
root.mainloop()
