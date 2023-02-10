import os 
import tqdm
import urllib
import urllib.request
import multiprocessing
import queue
from PIL import Image
import shutil
import math
import colorama
from imageai.Detection import ObjectDetection


# test
colorama.init()
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
#init colors

try:
    #check_modelyolo()
    execution_path = os.getcwd()
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, "\\model\\yolov3.pt"))
    print("[+]Loading Model...")
    detector.loadModel()
    print("[+]Model Loaded")
except:
    print("--------")
    
slash = '\\'
execution_path = os.getcwd()
src = execution_path + f"{slash}src"
output = execution_path + f"{slash}output"
detected = execution_path + f"{slash}detected{slash}"
driver_detected = execution_path + f"{slash}driver_detected{slash}"
car_size_k03 = execution_path + f"{slash}carsize_k0.3{slash}"


def check_modelyolo():
    try:
        if os.path.exists("/model/yolov3.pt"):
            print("[+] yolov3.pt exist")
        else:
            url = "https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/"
            destination = os.getcwd()+'/model/yolov3.pt'
            print("[+] MODEL DOWNLOADING yolo.h5 in model path")
            tqdm(urllib.request.urlretrieve(url, destination))
            print("[+] MODEL DOWNLOADED yolo.h5 in model path")
    except Exception as ex:
        print("[+] check yolo model source: https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5/", ex)



def worker(input_queue, stop_event): #worker for imageai
    while not stop_event.is_set():

        try:
            url = input_queue.get(True, 1)
            input_queue.task_done()
        except queue.Empty:
            continue

        #print('Started working on:', url)

        try:
            detect(url)
        except Exception as e:
            print(f"{RED}WORKER: {e}{RESET}")

        #print('Stopped working of:', url)

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

def driver_in(car, person):
    x1 , y1 , x2, y2 = car
    xx1, yy1, xx2, yy2 = person
    if x1 < xx1 and y1 < yy1 and x2 > xx2 and y2 > yy2:
        return True
    else:
        return False


def size_k(image, bbox_size):
    im = Image.open(image)
    image_width, image_height = im.size
    sqr = image_height * image_width
    x1,y1,x2,y2 = bbox_size
    rectangleArea = math.fabs(x1 - x2) * math.fabs(y1 - y2)
    return rectangleArea/sqr


def detect(path_file):
    flag = False

    person_count = 0
    im = Image.open(path_file)
    image_width, image_height = im.size  # let rectangleArea = Math.abs(x1 - x2) * Math.abs(y1 - y2); #square of ddbox
    sqr = image_height * image_width
    custom = detector.CustomObjects(person=True, car=True, bus=True, truck=True)
    temp = execution_path + '\\' + 'detected' + '\\' + path_file.split('\\')[-1]
    detections = detector.detectObjectsFromImage(
        custom_objects=custom,
        input_image=f"{path_file}",
        extract_detected_objects=False,
        output_image_path=temp,
        minimum_percentage_probability=50)
    for eachObject in detections:
        x1, y1, x2, y2 = eachObject["box_points"]
        rectangleArea = math.fabs(x1 - x2) * math.fabs(y1 - y2)
        k = rectangleArea / sqr
        print(f"{GREEN}", eachObject["name"], " : ", eachObject["percentage_probability"], " : ",
              eachObject["box_points"], " : ", k, "size_k", f"{RESET}")
        if eachObject["name"] == "car" or "bus" or "truck" and "person":
            if eachObject["name"] == "person":
                for detect in detections:
                    if (detect["name"] == "car" or "bus" or "truck") and (
                            0.2 < size_k(path_file, detect["box_points"])):
                        if driver_in(detect["box_points"], eachObject["box_points"]):
                            print(f"{RED} DRIVER in car's bbox !!!{RESET}")
                            shutil.copyfile(f"{path_file}", f"{driver_detected}{path_file.split(slash)[-1]}")
                            flag = True
                            continue

            person_count += 1
            if person_count <= 2 and not flag:
                flag = True
                print(f"{GREEN} <= 2 Persons with car but not sure", eachObject["name"], " : ",
                      eachObject["percentage_probability"], " : ", eachObject["box_points"], " : ", k, "size_k",
                      f"{RESET}")

            if k >= 0.3:
                shutil.copyfile(f"{path_file}", f"{car_size_k03}{path_file.split(slash)[-1]}")

    print(f"{YELLOW}{path_file}{RESET}")
    if flag:
        shutil.copyfile(f"{path_file}", f"{path_file.replace('src', 'output')}")
        # iterator for driver_detect()
    print("----------------------------")