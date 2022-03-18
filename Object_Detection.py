# GRIP Internship
# TASK-1 : Implement an object detector which identifies the classes of the objects in a real time video.
# Name : DINAKARAN
# Domain : Computer Vision and IOT


#import opencv and numpy library
import cv2
import numpy as np

# Threshold to detect object and nms is used for accuracy of boxes around objects
thres = 0.45
nms_threshold = 0.2

#Default Camera Capture
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
cap.set(10, 150)

##Importing the COCO dataset in a list
classNames= []
classFile = 'coco.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

#print(classNames)

##Configuring both SSD model and weights (assigning)
configPath = 'ssd_mobilenet_v3_large_coco_2022_03_02.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

##dnn-Inbuilt method of OpenCV
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

## using Detect method
while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold=thres)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1, -1)[0])
    confs = list(map(float, confs))
    #print(type(confs[0]))
    #print(confs)

    indices = cv2.dnn.NMSBoxes(bbox, confs, thres, nms_threshold)
    #print(indices)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        cv2.rectangle(img, (x, y),(x+w, h+y), color=(0, 255, 0), thickness=2)
        cv2.putText(img,classNames[classIds[i][0]-1].upper(), (box[0]+10, box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Output", img)
    cv2.waitKey(1)
