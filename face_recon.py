import requests
from io import BytesIO
from PIL import Image, ImageDraw
import cv2
import urllib3

import cognitive_face as CF

KEY = 'c568afc262db4b66a41636ce7441bf4f'  # Replace with a valid subscription key (keeping the quotes in place).
CF.Key.set(KEY)
# If you need to, you can change your base API url with:
#CF.BaseUrl.set('https://westcentralus.api.cognitive.microsoft.com/face/v1.0/')

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
CF.BaseUrl.set(BASE_URL)

# You can use this example JPG or replace the URL below with your own URL to a JPEG image.#
#img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
persongroupid="myfriends"
#CF.person_group.create(persongroupid,"SEX1") #for 8 faces
f=[0]*10
f[1]=CF.person.create(persongroupid,"p1")
f[2]=CF.person.create(persongroupid,"p2")
f[3]=CF.person.create(persongroupid,"p3")
f[4]=CF.person.create(persongroupid,"p4")
f[5]=CF.person.create(persongroupid,"p5")
f[6]=CF.person.create(persongroupid,"p6")
f[7]=CF.person.create(persongroupid,"p7")
f[8]=CF.person.create(persongroupid,"p8")
h=0
for j in range(1,9):
    w=f[j]
    for i in range(1,4):
        ob='/home/madhur/Desktop/'+str(j)+'/'+str(i)+'.jpeg'
        h=h+1
        #print(h)
        CF.person.add_face(ob,persongroupid,w['personId'])
#for i in range(1,4):
    #ob='/home/madhur/Desktop/3/'+str(i)+'.jpg'
    #im=Image.open(ob)
    #CF.person.add_face(ob,persongroupid,f2['personId'])
CF.person_group.train(persongroupid)
test='/home/madhur/Desktop/test1.jpeg'
fac=CF.face.detect(test)
print('no. of faces detected',len(fac))
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
print(k,"faces unknown")
print(d,'faces known')

