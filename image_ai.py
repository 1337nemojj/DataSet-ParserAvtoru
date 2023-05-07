import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import tqdm
# import urllib
import urllib.request
import multiprocessing
import queue
from PIL import Image
import shutil
import math
import colorama
# from imageai.Detection import ObjectDetection
import cv2
import numpy as np
import math
from PIL import Image

# test
colorama.init()
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
#init colors

# try:
#     #check_modelyolo()
#     execution_path = os.getcwd()
#     detector = ObjectDetection()
#     detector.setModelTypeAsYOLOv3()
#     detector.setModelPath(os.path.join(execution_path, "\\model\\yolov3.pt"))
#     print("[+]Loading Model...")
#     detector.loadModel()
#     print("[+]Model Loaded")
# except:
#     print("--------")
    

slash = '\\'
execution_path = os.getcwd()
src = execution_path + f"{slash}src"
output = execution_path + f"{slash}output"
detected = execution_path + f"{slash}detected{slash}"
driver_detected = execution_path + f"{slash}driver_detected{slash}"
car_size_k03 = execution_path + f"{slash}carsize_k0.3{slash}"



def size_k(image, bbox_size):
    im = Image.open(image)
    image_width, image_height = im.size
    sqr = image_height * image_width
    x1,y1,x2,y2 = bbox_size
    rectangleArea = math.fabs(x1 - x2) * math.fabs(y1 - y2)
    return rectangleArea/sqr

def detect(image_path):
    
    net = cv2.dnn.readNet("./model/yolov3.weights", "./model/yolov3.cfg")
    classes = ["car", "truck", "bus"]
    
    image = cv2.imread(image_path)

    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    output_layers = net.getUnconnectedOutLayersNames()
    layer_outputs = net.forward(output_layers)


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
                x1 = int(center_x - width / 2)
                y1 = int(center_y - height / 2)
                x2 = x1 + width
                y2 = y1 + height
                bbox = x1,y1,x2,y2
                k = width*height / image.shape[0]*image.shape[1] 
                print(f"confidence ~{classes[class_id]}\t: {confidence}; k:{size_k(image_path,bbox)}")
                if size_k(image_path,bbox) > 0.3:
                    # cv2.rectangle(image, (x1, y1), (x1+width, y1+height), (0, 255, 0), 2)
                    shutil.copyfile(f"{image_path}", f"{car_size_k03}{image_path.split(slash)[-1]}")
                    



# def detect(path_file):
#     flag = False

#     person_count = 0
#     # im = Image.open(path_file)
#     with Image.open(path_file) as im:
#         image_width, image_height = im.size  # let rectangleArea = Math.abs(x1 - x2) * Math.abs(y1 - y2); #square of ddbox
#         sqr = image_height * image_width
#         custom = detector.CustomObjects(person=True, car=True, bus=True, truck=True)
#         temp = execution_path + '\\' + 'detected' + '\\' + path_file.split('\\')[-1]
#         detections = detector.detectObjectsFromImage(
#             custom_objects=custom,
#             input_image=f"{path_file}",
#             extract_detected_objects=False,
#             output_image_path=temp,
#             minimum_percentage_probability=50)
#         for eachObject in detections:
#             x1, y1, x2, y2 = eachObject["box_points"]
#             rectangleArea = math.fabs(x1 - x2) * math.fabs(y1 - y2)
#             k = rectangleArea / sqr
#             print(f"{GREEN}", eachObject["name"], " : ", eachObject["percentage_probability"], " : ",
#                 eachObject["box_points"], " : ", k, "size_k", f"{RESET}")
#             if eachObject["name"] == "car" or "bus" or "truck" and "person":
#                 if eachObject["name"] == "person":
#                     for detect in detections:
#                         if (detect["name"] == "car" or "bus" or "truck") and (
#                                 0.2 < size_k(path_file, detect["box_points"])):
#                             if driver_in(detect["box_points"], eachObject["box_points"]):
#                                 print(f"{RED} DRIVER in car's bbox !!!{RESET}")
#                                 shutil.copyfile(f"{path_file}", f"{driver_detected}{path_file.split(slash)[-1]}")
#                                 flag = True
#                                 continue

#                 person_count += 1
#                 if person_count <= 2 and not flag:
#                     flag = True
#                     print(f"{GREEN} <= 2 Persons with car but not sure", eachObject["name"], " : ",
#                         eachObject["percentage_probability"], " : ", eachObject["box_points"], " : ", k, "size_k",
#                         f"{RESET}")

#                 if k >= 0.3:
#                     shutil.copyfile(f"{path_file}", f"{car_size_k03}{path_file.split(slash)[-1]}")

#         print(f"{YELLOW}{path_file}{RESET}")
#         if flag:
#             shutil.copyfile(f"{path_file}", f"{path_file.replace('src', 'output')}")
#             # iterator for driver_detect()
        
#         print("----------------------------")

# def check_modelyolo():
#     try:
#         if os.path.exists("/model/yolov3.pt"):
#             print("[+] yolov3.pt exist")
#         else:
#             url = "https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/"
#             destination = os.getcwd()+'/model/yolov3.pt'
#             print("[+] MODEL DOWNLOADING yolo.h5 in model path")
#             tqdm(urllib.request.urlretrieve(url, destination))
#             print("[+] MODEL DOWNLOADED yolo.h5 in model path")
#     except Exception as ex:
#         print("[+] check yolo model source: https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5/", ex)


# C:\Users\nemojj\Desktop\DataSet-ParserAvtoru\src\1\mitsubishi\l200__1116132758-a50baaff\1bc7534f7a891600af668878cc9bbbdc.jpg
def worker(input_queue, stop_event): #worker for imageai
    while not stop_event.is_set():

        try:
            url = input_queue.get(True, 1)
            input_queue.task_done()
        except queue.Empty:
            continue

        print('Started working on:', url)

        try:
            detect(url)
        except Exception as e:
            print(f"{RED}WORKER: {e}{RESET}")

        print('Stopped working of:', url)

def master(urls):
    input_queue = multiprocessing.JoinableQueue()
    stop_event = multiprocessing.Event()
    workers = []


    # Create workers. cpu_count() / 2
    for i in range(4):
        p = multiprocessing.Process(target=worker, args=(input_queue, stop_event))
        workers.append(p)
        p.start()

    # Distribute work.
    for url in urls:
        input_queue.put(url)

    # Wait for the queue to be consumed.
    input_queue.join()

    # Ask the workers to quit.
    stop_event.set()

    # Wait for workers to quit.
    for w in workers:
        w.join()

    print('Done')

# def driver_in(car, person):
#     x1 , y1 , x2, y2 = car
#     xx1, yy1, xx2, yy2 = person
#     if x1 < xx1 and y1 < yy1 and x2 > xx2 and y2 > yy2:
#         return True
#     else:
#         return False
