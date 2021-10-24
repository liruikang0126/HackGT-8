from collections import namedtuple
from django.shortcuts import render

import numpy as np
import urllib
import json
import cv2
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import base64
import json

from .models import merchant
from .models import image
from django.core import serializers
from django.core.files.storage import FileSystemStorage




face_detector = "haarcascade_frontalface_default.xml"

# Create your views here.

def home(request):
    return render(request, 'index.html')
 

def recog(request):
    default = {"safely executed": False}
 
    if request.method == "POST":
        if request.FILES.get("image", None) is not None: 
            image_to_read = read_image(stream = request.FILES["image"])
 

 
 
        image_to_read = cv2.cvtColor(image_to_read, cv2.COLOR_BGR2GRAY) 
        detector_value = cv2.CascadeClassifier(face_detector) 
 
        
        values = detector_value.detectMultiScale(image_to_read,
                                                 scaleFactor=1.1,
                                                 minNeighbors = 5,
                                                 minSize=(30,30),
                                                 flags = cv2.CASCADE_SCALE_IMAGE)
 
        
        values=[(int(a), int(b), int(a+c), int(b+d)) for (a,b,c,d) in values]
 
        default.update({"#of_faces": len(values),
                        "faces":values,
                        "safely_executed": True })
 
    return JsonResponse(default)

def getData(request):
    default = {"safely executed": False}
    if request.method == "POST":
        js = get_table()
        #("----------")
        #print(json)
        data = []
        for item in json.loads(js):
            #print(item)
            buf = {}
            buf['x'] = item['fields']['name']
            buf['value'] = item['fields']['current_queue_size']
            buf['time'] = item['fields']['approximate_queue_waiting_time']
            buf['id'] = item['pk']
            data.append(buf)
        #print(data)
        '''default['data'] = [[
    {"x": "Mandarin", "value": 15, "id": 1},
    {"x": "English", "value": 20, "id": 2},
    {"x": "Hindustani", "value": 10, "id": 3},
    {"x": "Spanish", "value": 8, "id": 4},
    {"x": "Arabic", "value": 1, "id": 5},
    {"x": "Malay", "value": 1, "id": 6},
    {"x": "Russian", "value": 3, "id": 7},
    {"x": "Bengali", "value": 45, "id": 8},
    {"x": "Portuguese", "value": 6, "id": 9},
    {"x": "French", "value": 28, "id": 10},
    {"x": "Hausa", "value": 30, "id": 11},
    {"x": "Punjabi", "value": 3, "id": 12},
    {"x": "Japanese", "value": 3, "id": 13},
    {"x": "German", "value": 7, "id": 14},
    {"x": "Persian", "value": 35, "id": 15}
    ]]'''
        default['data'] = data
        return JsonResponse(default)

def recognition(request):
    default = {"safely executed": False}
    print(request)
 
    
    if request.method == "POST":
        print(request.FILES)
        if request.FILES["image"] is not None: 
            new_img = image(
            img=request.FILES.get("image") )
            image_to_read = read_image(stream = request.FILES["image"])
            new_img.save()





            '''img = request.FILES["image"]
            fs = FileSystemStorage()
            filename = fs.save(img.name, img)
            print(fs.url(filename))'''

            
        else:
            default["error_value"] = "no image find"
            return JsonResponse(default)
 
        imgGray = cv2.cvtColor(image_to_read, cv2.COLOR_BGR2GRAY) 
        detector_value = cv2.CascadeClassifier(face_detector) 
 
        
        values = detector_value.detectMultiScale(imgGray,
                                                 scaleFactor=1.1,
                                                 minNeighbors = 5,
                                                 minSize=(60,60),
                                                 flags = cv2.CASCADE_SCALE_IMAGE)
 
        
        values=[(int(a), int(b), int(a+c), int(b+d)) for (a,b,c,d) in values]
 
        
        for (w,x,y,z) in values:
            cv2.rectangle(image_to_read,(w,x), (y,z), (0, 255, 0), 2)
 
        retval, buffer_img= cv2.imencode('.jpg', image_to_read) 
        img64 = base64.b64encode(buffer_img)
        img64=str(img64, encoding='utf-8') 
        default["img64"] = img64  
    return JsonResponse(default)



def read_image(stream=None, url=None):

    if stream is not None:
        data_temp = stream.read()

    image = np.asarray(bytearray(data_temp), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def queueSize_to_time(merchant_id):
    merchant1 = merchant.objects.get(merchant_id = merchant_id)
    current_queue_size = merchant1.current_queue_size
    waiting_time_per_person = merchant1.waiting_time_per_person
    total_waiting_time = current_queue_size * waiting_time_per_person
    return int(total_waiting_time)


def update_current_queue_size(run_model_result, merchant_id):
    merchant1 = merchant.objects.get(merchant_id = merchant_id)
    merchant1.set_current_queue_size(run_model_result)
    merchant1.save()




"""Delete all data in the current table to be ready to add Merchants"""
merchant.objects.all().delete()

"""Start adding! The food names are from 'https://gothamist.com/food/20-quintessential-taiwanese-night-market-street-foods' """



merchant_list = []

name_list = ["Stinky Tofu (Fries)", "Black Pepper Buns", "Ice Cream Runbing", "Deep Fried Taro Ball",
            "Aiyu Jelly Drink", "Broiled Squid", "Dorayaki", "Coffin Bread", "Fish ball", "Fried chicken",
            "Guabao", "Oyster omelet", "Oyster vermicelli", "Pork blood cake", "Mochi"]

id_list = list(range(1,16))


waiting_time_pp_list = [1, 2, 1, 3, 0.5, 2, 1, 2, 2.5, 5, 3, 4, 5, 2, 1.5]    # unit = minute

queue = [15,20,10,8,1,1,35,17,28,10,3,7,20, 27, 15]
for id in id_list:
    merchant_info = merchant()
    merchant_info.name = name_list[id - 1]
    merchant_info.merchant_id = id
    merchant_info.current_queue_size = queue[id - 1]
    merchant_info.waiting_time_per_person = waiting_time_pp_list[id - 1]
    #merchant_info.approximate_queue_waiting_time = queue[id - 1] * waiting_time_pp_list[id - 1]
    merchant_info.save()
    merchant_list.append(merchant_info)

"""Now fill in the approximate waiting time"""

for merchants in merchant_list:
    merchants.approximate_queue_waiting_time = queueSize_to_time(merchants.merchant_id)
    #print(merchants.approximate_queue_waiting_time)
    merchants.save()

def get_table():
    m = serializers.serialize("json", merchant.objects.all())
    #print(f'{m.name}: Current waiting time is {m.approximate_queue_waiting_time} minute(s). Last update time: {m.last_update_time.strftime("%m/%d/%y %I:%M %p")}.')
    return m

