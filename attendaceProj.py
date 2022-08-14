import cv2
import numpy as np
import face_recognition
import os
from datetime import date
from datetime import datetime
import pywhatkit
import  time
import pyttsx3 as Speech

engine = Speech.init()

#---------------------------------
# SEM 3 MINI PROJECT BEGINS!------
#---------------------------------

#STEP 1: Import all the images and convert them to RGB

path = 'ImagesAttendance'
images = [] # To Fetch ALl Images From The Folder
classNames = []
myList = os.listdir(path)
print(myList)

for cls in myList:
    curImg = cv2.imread(f'{path}/{cls}') # cl = name of img
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0]) #TO REMOVE .JPG EXTENSIONS

print(classNames)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

encodeListKnown = findEncodings(images)
print(len(encodeListKnown)) #Number of Images or Number of items in Directory
print('ENCODEINGS SUCCESSFUL')

#ATTENDANCE CLASS:
Today = date.today()
def markAttendance(name):

    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0]) #FIRST ELEMENT OF ENTRY
        if name not in nameList:
            now = datetime.now()
            TimeString = now.strftime('%H:%M:%S')
            DateString = Today.strftime('%B %d %Y')
            f.writelines(f'\n{name},{DateString},{TimeString}')

def WAmsg(name,Phnum):
    now = datetime.now()
    dt = now.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S")
    pywhatkit.sendwhatmsg_instantly(Phnum, "Hi " + name + " Attendance date and time: " + dt + " " + tm)



#STEP 2: INITIALIZE WEBCAM TO COMPARE IMAGE

cap = cv2.VideoCapture(0)


while True:
    success, img = cap.read()
    imgSmall = cv2.resize(img,(0,0),None,0.25,0.25) #Reducing img size to speed the process (0.25,0.25) = 1/4th the size of image
    imgSmall = cv2.cvtColor(imgSmall,cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgSmall)
    encodeCurFrame = face_recognition.face_encodings(imgSmall , facesCurFrame)



    #STEP 3 : FINDING MATCHES
    for encodeFace,faceLoc in zip(encodeCurFrame,facesCurFrame): #it will grab 1 by 1 face locations form FacesCurFrame list and encode them in encodesCurFrame List
        matches = face_recognition.compare_faces(encodeListKnown , encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
       # print(faceDis)

        matchIndex = np.argmin(faceDis)


        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)
            engine.say("Hii " + name + " Welcome to Shivajirao S Jhondale College of Engineering")
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x2 = y1*4,x2*4,y1*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)




            markAttendance(name)

            now = datetime.now()
            if name == "MAHESH":
                PhNum = "+919076107717"
            if name == "MUMMY":
                PhNum = "+918693857322"
            if name == "LOKESH":
                PhNum = "+917710874612"
            if name=="PAPA":
                PhNum = "+919768347373"

            minExe = now.strftime("")

            WAmsg(name,PhNum)



    cv2.imshow('webcam',img)
    cv2.waitKey(1)



    # ---------------------------------
    # SEM 3-4 MINI PROJECT ENDS!------
    # ©MAHESH WAGH
    # ---------------------------------








