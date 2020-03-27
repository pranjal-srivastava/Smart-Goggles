import picamera
from  picamera.array import  PiRGBArray
import cv2
import time
import numpy as np
import boto3
import speak2
import requests
import RPi.GPIO as GPIO
import dlib
from io import BytesIO
from PIL import Image, ImageDraw
import urllib3
import cognitive_face as CF


GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP) #button
TRIG=22
ECHO=24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
detector = dlib.get_frontal_face_detector()

def image(filename):
	with open (filename,'rb') as imgfile:
		return imgfile.read()

def object_recog():
    print ('object detection')
    client=boto3.client('rekognition')
    imgurl ='tarpimg.jpg';
    imgbytes = image(imgurl)
    rekresp = client.detect_labels(Image={'Bytes': imgbytes},
                               MinConfidence=70)
    flag=0
    for label in rekresp['Labels']:
        print (label['Name'])
        speak2.say(label['Name'])
        flag=1
    if flag==0:
            
      speak2.say('no object found')

def message():
 print ("message activated")  
 response = requests.get("http://poxy.16mb.com/sendpranav.php?mob=9790001196&message=I am at VIT VELLORE,SOS")
 speak2.say("MESSAGE SENT")
 print(response.text)
 

def landmarks():
 print ("entering landmarks")
 speak2.say("TT , SJT , GALAXY CINEMA")
 print ("entering landmarks")


def face_detect(image):
     img=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
     detections = detector(img, 0)
     for k,d in enumerate(detections):
       return 1
     return 0  

def face_recog():
    print "Recognising faces"
    KEY = 'c568afc262db4b66a41636ce7441bf4f'  # Replace with a valid subscription key (keeping the quotes in place).
    CF.Key.set(KEY)
    # If you need to, you can change your base API url with:
    #CF.BaseUrl.set('https://westcentralus.api.cognitive.microsoft.com/face/v1.0/')

    BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
    CF.BaseUrl.set(BASE_URL)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    persongroupid="myfriends"
    test='./tarpimg.jpg'
    fac=CF.face.detect(test)
    print('no. of faces detected',len(fac))
    if(len(fac)!=0):
        faceid=[]
        for j in range(len(fac)):
            ind=fac[j]
            faceid.append(ind['faceId'])
        print(faceid)
        results=CF.face.identify(faceid,persongroupid)
        print(results)
        k=0
        d=0
        for i in range(len(results)):
            res=results[i]
            res1=res['candidates']
            if(len(res1)==0):
                k=k+1
            else:
                d=d+1
                res2=res1[0]
                res3=CF.person.get(persongroupid,res2['personId'])
                print(res3['name'])
                speak2.say(res3['name'])
        print(k,"faces unknown")
        print(d,'faces known')
        if k>=1:
            return 1
        else:
            return 0
    #-----------------------------------------------------
def face_analysis():
 print ("analysing face")
 client=boto3.client('rekognition')
 imgurl ='tarpimg.jpg';
 imgbytes = image(imgurl)
 rekresp = client.detect_faces(Image={'Bytes': imgbytes},Attributes=['ALL'])
 if len(rekresp['FaceDetails'])>0:
  gender= rekresp['FaceDetails'][0]['Gender']['Value']
  age= rekresp['FaceDetails'][0]['AgeRange']['High']
  age_l=rekresp['FaceDetails'][0]['AgeRange']['Low']
  emotion=rekresp['FaceDetails'][0]['Emotions'][0]['Type']
  eyeglasses=rekresp['FaceDetails'][0]['Eyeglasses']['Value']
  print gender,age_l,age,emotion,eyeglasses
  speak2.say("The person is a "+gender)
  speak2.say("Age is between "+str(age_l)+" to "+str(age))
  speak2.say("person is "+emotion)
  if eyeglasses==True:
   speak2.say("Wearing eyeglasses")
 else:
        speak2.say('No person')
          
    
    
    
 
camera=picamera.PiCamera()
camera.resolution=(640,480)
camera.brightness=70
camera.contrast=60
#camera.exposure_mode='backlight'
output=PiRGBArray(camera,size=(640,480))
time.sleep(2)

face_flag=0

for frame in camera.capture_continuous(output,format="bgr",use_video_port=True):
    frame=frame.array
    count_long=0
    input_state = GPIO.input(18)
    
    while input_state == False:
        input_state = GPIO.input(18)
        print('Button Pressed')
        time.sleep(0.2)
        count_long=count_long+1;

    if count_long<10 and count_long>2:
        message()

    elif count_long>=10:
            landmarks()    
    
    
    GPIO.output(TRIG,False)
    #print "Waiting...."


    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)

    while GPIO.input(ECHO)==0:
        pulse_start=time.time()

    while GPIO.input(ECHO)==1:
        pulse_end=time.time()

    pulse_duration=pulse_end-pulse_start
    distance=pulse_duration*17150
    distance=round(distance,2)
    

        

    if distance<25:
        
            print "ultrasonic sensor"
            cv2.imwrite('tarpimg.jpg',frame)
            if face_detect(frame)==1:
                    print "face detected"
                    face_flag=face_recog()           #madhur-face-api
                    if face_flag==1:
                      speak2.say("analysing unknown face")
                      
                      face_analysis()        #dheer ka face analyis
            else:
                    print "no face"
                    object_recog()
                    

            
    output.truncate(0);        
