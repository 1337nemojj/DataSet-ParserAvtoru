import cv2
import numpy as np
import math
from PIL import Image

net = cv2.dnn.readNet("./model/yolov3.weights", "./model/yolov3.cfg")

with open("./model/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]


classes_names = ["car", "truck", "bus"]
image_path = "./src/111/lexus/es__1118027496-54dc8b31/1e4a69b58cf25bd353c7abb4c35ca579.jpg"#C:\Users\nemojj\Desktop\DataSet-ParserAvtoru\src\111\lexus\es__1118027496-54dc8b31\1e4a69b58cf25bd353c7abb4c35ca579.jpg
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
        if confidence > 0.7 and classes[class_id] in classes_names:
            
            center_x = int(detection[0] * image.shape[1])
            center_y = int(detection[1] * image.shape[0])
            width = int(detection[2] * image.shape[1])
            height = int(detection[3] * image.shape[0])
            x1 = int(center_x - width / 2)
            y1 = int(center_y - height / 2)
            x2 = x1 + width
            y2 = y1 + height
            bbox = x1,y1,x2,y2
            k = width*height / image.shape[0]*image.shape[1] 
            print(f"confidence ~{classes[class_id]}\t: {confidence}; k:{size_k(image_path,bbox)}")
            if size_k(image_path,bbox) > 0.3:
                cv2.rectangle(image, (x1, y1), (x1+width, y1+height), (0, 255, 0), 2)


cv2.imshow("Object detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
