import cv2
import numpy as np
import os
import sqlite3
import time

COURSE = ""
nameList = []

conn=sqlite3.connect("FaceBase.db")

def __del__(self):
    conn.close()

def __init__(self):
    conn=sqlite3.connect("FaceBase.db")
    COURSE = ""
    nameList = []


def startRecognize(lesson, lecture_date):
    conn=sqlite3.connect("FaceBase.db")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainner/trainner.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    COURSE = ""

    nameList.clear()
    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video widht
    cam.set(4, 480) # set video height
    # Define min window size to be recognized as a face
    minW = 0.1*cam.get(3)
    minH = 0.1*cam.get(4)
    while True:
        ret, img =cam.read()
        img = cv2.flip(img, 1) # Flip vertically
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.3, # For more reliable results, scaleFactor = 1.05
            minNeighbors = 5,  # and minNeighbors = 3
            minSize = (int(minW), int(minH)),
           )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

            profile=getProfile(id)
            print(profile[2])
            temp_name = profile[2]
            temp_id = profile[1]
            temp_age = profile[3]
            temp_gender = ""


            if (confidence >= 40):
                temp_name = "Unknown"
                temp_id = 0
                temp_age = 0
                temp_gender = 0

            if(profile!=None):
                if(confidence<=40):
                    markAttendance(str(profile[1]), str(profile[2]), lesson, lecture_date)
                cv2.putText(
                        img, 
                        str(temp_id), 
                        (x+5,y-5), 
                        font, 
                        1, 
                        (255,255,255), 
                        2
                       )
                cv2.putText(
                        img, 
                        str(100-confidence), 
                        (x+5,y+h-5), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                       )  
                cv2.putText(
                        img, 
                        str(temp_id), 
                        (x,y+h+30), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                       ) 
                cv2.putText(
                        img, 
                        str(temp_name), 
                        (x,y+h+60), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                       )  
                cv2.putText(
                        img, 
                        str(temp_age), 
                        (x,y+h+90), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                       )  
                cv2.putText(
                        img, 
                        str(temp_gender), 
                        (x,y+h+120), 
                        font, 
                        1, 
                        (255,255,0), 
                        1
                       )  

        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()

def markAttendance(st_id, st_name, lesson, lecture_date):
    if st_id not in nameList:
        print("eseseses")
        nameList.append(st_id)
        # Recording to database
        cmd="INSERT INTO ATTENDANCE (STUDENT_ID, STUDENT_NAME, LESSON, ATTENDANCE_DATE) VALUES (" +st_id+", '"+st_name+"', '"+lesson+"', '" + str(lecture_date) + str(time.strftime (" %H:%M:%S")) + "');"
        cursor=conn.execute(cmd)
        conn.commit()

def getProfile(id):
    cmd="SELECT * FROM STUDENT WHERE STUDENT_ID ="+str(id)
    cursor=conn.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    return profile