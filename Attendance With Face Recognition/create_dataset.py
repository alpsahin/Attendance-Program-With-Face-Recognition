import cv2
import sqlite3
import numpy as np

from keras.preprocessing.image import ImageDataGenerator,array_to_img, img_to_array,load_img


STUDENT_ID=""
NAME=""
AGE=""
GENDER=""

def insertOrUpdate(STUDENT_ID, NAME, AGE, GENDER):
    conn=sqlite3.connect("FaceBase.db")
    cmd="SELECT * FROM STUDENT WHERE ID="+str(STUDENT_ID)
    cursor=conn.execute(cmd)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==""):
        cmd="UPDATE STUDENT SET Name="+str(NAME)+"WHERE ID="+str(STUDENT_ID)
    else:
        cmd="INSERT INTO STUDENT(STUDENT_ID, NAME, AGE, GENDER) Values("+str(STUDENT_ID)+",'"+str(NAME)+"',"+str(AGE)+",'"+str(GENDER)+"')"
        conn.execute(cmd)
        conn.commit()
        conn.close()

"""STUDENT_ID=input('enter your student id')
NAME=input('enter your name')
AGE=input('enter your age')
GENDER=input('enter your GENDER')
insertOrUpdate(STUDENT_ID, NAME, AGE, GENDER)
"""
def startCreate(std_id, std_name, std_age, std_gender):
    STUDENT_ID=std_id
    NAME=std_name
    AGE=std_age
    GENDER=std_gender
    insertOrUpdate(std_id, std_name, std_age, std_gender)

    cam = cv2.VideoCapture(0)
    detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    sampleNum=0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detecting is here
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            #incrementing sample number 
            sampleNum=sampleNum+1
            #saving the captured face in the dataset folder
            cv2.imwrite("dataSet/User."+STUDENT_ID +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
            # keras data augmentation
            datagen =ImageDataGenerator( rotation_range=40, width_shift_range=0.2, height_shift_range=0.2, brightness_range=None, shear_range=0.2, zoom_range=0.2, channel_shift_range=0.0, fill_mode='nearest', cval=0.0, horizontal_flip=True, vertical_flip=False)
            img=load_img("dataSet/User."+STUDENT_ID +'.'+ str(sampleNum) + ".jpg")
            x=img_to_array(img)
            x=x.reshape((1,)+x.shape)
            i=0
            for batch in datagen.flow(x,batch_size=1,save_to_dir="dataSet",save_prefix="User."+STUDENT_ID +'._'+ str(sampleNum),save_format="jpg"):
                i+=1
                if i>15:
                    break
            
            img = np.array(img)
            cv2.imshow('frame', img)
            
        #wait for 100 miliseconds 
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 30
        elif sampleNum>30:
            break
    cam.release()
    cv2.destroyAllWindows()