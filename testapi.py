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
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
persongroupid="myfriends"
test='/home/madhur/Desktop/test1.jpeg' #add test location
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