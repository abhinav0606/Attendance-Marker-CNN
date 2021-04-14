import cv2
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import Dropout
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import MaxPooling2D
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
train_dir="train"
test_dir="test"
# datagenerator
train_data_gen=ImageDataGenerator(1./255)
test_data_gen=ImageDataGenerator(1./255)
# creating generators
train_generators=train_data_gen.flow_from_directory(
    "/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Train",target_size=(48,48),batch_size=64,color_mode="grayscale",
    class_mode="categorical"
)
test_generators=test_data_gen.flow_from_directory(
    "/home/abhinav/PycharmProjects/CNN_ATTENDENCE_MARKER/Dataset/Test",target_size=(48,48),batch_size=64,color_mode="grayscale",
    class_mode="categorical"
)

# creating the emotional model
model=Sequential()
model.add(Conv2D(32,kernel_size=(3,3),input_shape=(48,48,1),activation='relu'))
model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Conv2D(128,kernel_size=(3,3),activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Conv2D(128,kernel_size=(3,3),activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(64,activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(2,activation="softmax"))

# compiling phase

model.compile(loss="categorical_crossentropy",optimizer=Adam(lr=0.0001,decay=1e-6),metrics=["accuracy"])
model.fit(
    train_generators,
    epochs=50,
    validation_data=test_generators
)
model.save("CNN_ATTENDENCE.h5")
capture=cv2.VideoCapture(0)
haarcascade=cv2.CascadeClassifier("frontal_face.xml")
while True:
    ret,frame=capture.read()
    frame=cv2.flip(frame,1)
    gray_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    face=haarcascade.detectMultiScale(gray_frame,1.3,5)
    for (x,y,w,h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),thickness=3)
        cropped_gray_frame=gray_frame[y:y+h,x:x+w]
        new_size_frame = np.expand_dims(np.expand_dims(cv2.resize(cropped_gray_frame, (48,48)), -1), 0)
        prediction=model.predict(new_size_frame)
        index = int(np.argmax(prediction))
        print(index)
        print(prediction)
        cv2.imshow("Frame",cropped_gray_frame)
    if cv2.waitKey(1)==13:
        break
capture.release()
cv2.destroyAllWindows()
