import cv2
import numpy as np
import math
from PIL import Image

net = cv2.dnn.readNet("./model/yolov3.weights", "./model/yolov3.cfg")

classes = ["car", "truck", "bus"]
image_path = "./src/lexus/lexus/ct__1117283571-88dbf6a9/0c62ce20131882dd128a12393b868446.jpg"
image = cv2.imread(image_path)

blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)

# Run forward pass to get output from network
output_layers = net.getUnconnectedOutLayersNames()
layer_outputs = net.forward(output_layers)


def size_k(image, bbox_size):
    im = Image.open(image)
    image_width, image_height = im.size
    sqr = image_height * image_width
    x1,y1,x2,y2 = bbox_size
    rectangleArea = math.fabs(x1 - x2) * math.fabs(y1 - y2)
    return rectangleArea/sqr

for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.7 and classes[class_id] in ["car", "truck", "bus"]:
            
            center_x = int(detection[0] * image.shape[1])
            center_y = int(detection[1] * image.shape[0])
            width = int(detection[2] * image.shape[1])
            height = int(detection[3] * image.shape[0])
            x = int(center_x - width / 2)
            y = int(center_y - height / 2)
            cv2.rectangle(image, (x, y), (x+width, y+height), (0, 255, 0), 2)
            k = width*height / image.shape[0]*image.shape[1]
            print(f"confidence {classes[class_id]}\t: {confidence}; {x}:{y}; {width}:{height}; k:{k}"  )

cv2.imshow("Object detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
