import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import base64
import shutil
import urllib.request
############
import multiprocessing
import queue
from imageai.Detection import ObjectDetection
from PIL import Image
import tqdm
############
import colorama
import requests
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from bs4 import BeautifulSoup
import time

import wget
import chromedriver_autoinstaller
import math

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

#checks
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
"""
[+] NOTES [+]
    OLD VERSION!!!
installation ImageAi:
Python3.7.6
pip install tensorflow==2.4.0
pip install tensorflow-gpu==2.4.0
pip install keras==2.4.3 numpy==1.19.3 pillow==7.0.0 scipy==1.4.1 h5py==2.10.0 matplotlib==3.3.2 opencv-python keras-resnet==0.2.0
pip install imageai --upgrade
    NEW VERSION
pip install cython pillow>=7.0.0 numpy>=1.18.1 opencv-python>=4.1.2 torch>=1.9.0 --extra-index-url https://download.pytorch.org/whl/cpu torchvision>=0.10.0 --extra-index-url https://download.pytorch.org/whl/cpu pytest==7.1.3 tqdm==4.64.1 scipy>=1.7.3 matplotlib>=3.4.3 mock==4.0.3
pip install cython pillow>=7.0.0 numpy>=1.18.1 opencv-python>=4.1.2 torch>=1.9.0 --extra-index-url https://download.pytorch.org/whl/cu102 torchvision>=0.10.0 --extra-index-url https://download.pytorch.org/whl/cu102 pytest==7.1.3 tqdm==4.64.1 scipy>=1.7.3 matplotlib>=3.4.3 mock==4.0.3



models ImageAi:
https://imageai.readthedocs.io/en/latest/detection/index.html 
link: https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5/


link: https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5/
https://auto.ru/sankt-peterburg/cars/vendor-foreign/all/?year_to=2022&price_from=18000000
https://auto.ru/sankt-peterburg/cars/bmw/all/?year_to=2022&price_from=8000000

put in /model/yolo.h5
then launch

"""
# test
colorama.init()
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW
#init colors

li = []
headers_response = []
webm_links_1200x900n = []
links = []
names = []
clr_names = []
already_loaded_img = []
count = 0
i = 0
page_lit = "&page="
page_int = 1
links_clear = []
tokens_list = []
wrong_symbols = ['\\', '|', '/', '*', '?', '"', '<', '>']
comp_count = 0
slash = '\\'
images_list = []
# paths
execution_path = os.getcwd()
src = execution_path + f"{slash}src"
output = execution_path + f"{slash}output"
detected = execution_path + f"{slash}detected{slash}"
driver_detected = execution_path + f"{slash}driver_detected{slash}"
car_size_k03 = execution_path + f"{slash}carsize_k0.3{slash}"
# check paths
try:
    os.mkdir(driver_detected)
    os.mkdir(car_size_k03)
    os.mkdir(src)
    os.mkdir(output)
    os.mkdir(detected)
except Exception as ex:
    print("FOLDER: ", ex)

#del empty dirs
def del_empty_dirs(path):
    for d in os.listdir(path):
        a = os.path.join(path, d)
        if os.path.isdir(a):
            del_empty_dirs(a)
            if not os.listdir(a):
                os.rmdir(a)
                print(a, ' DELETED')


def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)


def find_index_path(str):
    return ''.join(x for x in str if x.isdigit())


def name_checker(name):
    tempa = ""
    fl = False
    for sym in wrong_symbols:
        if sym in name:
            tempa = name.replace(sym, '')
            fl = True
    if fl:
        return tempa
    else:
        return name

def init_project ():
    try:
        while True:
            print(f"[?]{GRAY}NAME PROJECT:{RESET}")
            project_name_e = input()
            project_name = path + "\\" + project_name_e
            if os.path.exists(f"{project_name}"):
                print(f"[+]{GREEN}PROJECT {project_name} CREATED{RESET}")
                return project_name
                
            try:
                os.mkdir(f"{project_name}")
            except Exception as ex:
                print(ex)

            if os.path.exists(f"{project_name}"):
                print(f"[+]{GREEN}PROJECT {project_name} ALREADY CREATED{RESET}")
                break
    except Exception as ex:
        print(ex)


def main_parser(path):

    chromedriver_autoinstaller.install()

    global project_name, temp
    li = []
    webm_links_1200x900n = []
    already_loaded_img = []
    page_lit = "&page="
    page_int = 1
    links_clear = []
    index = 0
    project_name = "DEFAULT PROJECT"
    print(f"[?]{GRAY}avto.ru LINK WITH FILTERS aka https://auto.ru/cars/used/?catalog_filter=mark%3DBMW%...{RESET}")
    result = []
    row = True
    while row:
        row = input()
        if row:
            result.append(row)
    print(result)
    # create projects
    project_name = init_project()


    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("no-sandbox")
    chrome_options.add_argument("disable-dev-shm-usage")
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("log-level=3")
    chrome_options.add_argument(f"user-agent={useragent}")

    try:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        print(f"{GREEN}LAUNCH CHROME")

        for ent in result:
            url = f"{ent}{page_lit}{page_int}"
            driver.get(url)
            time.sleep(1.5)
            cur_link = driver.current_url
            print(f"[+]WORK WITH {cur_link}{RESET}")

            while "captcha" in driver.current_url:
                print(f"{RED}\r[!]CAPTCHA DETECT OR SMTH NOT GOOD HAPPEND sleep{RESET}")
                time.sleep(10)
            print("CAPTCHA SOLVED")
            time.sleep(1)
            #capthca geo tag

            current_working = driver.current_url

            while "captcha" in driver.current_url:
                print(f"{RED}\r[!]CAPTCHA DETECT OR SMTH NOT GOOD sleep{RESET}")
                time.sleep(10)
            print(f"{GREEN}[+]CAPTCHA SOLVED{RESET}")

            try:
                print(f"{GREEN}[+]SCROLLING{RESET}")
                try:
                    while True:
                        scroll_pause_time = 4
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        try:
                            element = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CLASS_NAME, "ListingPagination__moreButton")))
                            time.sleep(3)
                        except Exception as e:
                            print(e)  # Для отладки, после удалить
                            continue  # Не нашли элемент, попробуем на следующей итерации

                        actions = ActionChains(driver)
                        actions.move_to_element(element).perform()

                        try:
                            time.sleep(scroll_pause_time)
                            element.click()
                        except WebDriverException:
                            soup = BeautifulSoup(driver.page_source, 'lxml')
                            print(soup.prettify())

                        try:
                            time.sleep(2)
                            requiredHtml = driver.page_source
                            soup = BeautifulSoup(requiredHtml, "html.parser")
                            links = soup.findAll('a', class_='Link ListingItemTitle__link')
                            try:
                                page = soup.findAll('button',
                                                    class_='Button Button_color_blue Button_size_s Button_type_button Button_width_default ListingPagination__moreButton')
                                page_int += 1
                                print(f"{YELLOW}[+]PAGE: {page_int} : {driver.current_url}{RESET}")
                            except Exception as ex:
                                print(f"{YELLOW}[!]CANT FIND SHOW MORE BUTN or {ex}{RESET}")
                                break
                            try:
                                if page:
                                    print("[+]links: ", len(links))
                                    for i in links:
                                        # names.append(i.text.replace('/', ' '))
                                        links_clear.append(i.attrs.get('href'))
                                    links.clear()
                                    print(f"{GREEN}[+]FETCH PAGE'S LINKS{RESET}")
                                else:
                                    print(
                                        f"{RED}[!]ERROR PAGE OR PAGES FINISHED{RESET}")  # class="Spinner Spinner_visible Spinner_color_red Spinner_size_l" load more after pages

                                    SCROLL_PAUSE_TIME = 2
                                    last_height = driver.execute_script("return document.body.scrollHeight")
                                    # check
                                    try:
                                        time.sleep(1)
                                        page = soup.findAll('button',
                                                            class_='Button Button_color_blue Button_size_s Button_type_button Button_width_default ListingPagination__moreButton')
                                    except Exception as ex:
                                        print(ex)
                                    break
                            except Exception as ex:
                                print(ex)
                        except Exception as ex:
                            print(ex)
                except Exception as ex:
                    print(ex)
                finally:
                    li = [i for n, i in enumerate(links_clear) if i not in links_clear[:n]]
                    print(f"{YELLOW}li {len(li)} ; PAGES : {page_int}{RESET}")
                    # check complete file by duble -> del duble in li from complete !!!!!!!!!!!!
                    with open(f"{project_name}\\fetched.txt", "w") as s:
                        for i in li:
                            s.write(i + '\n')

            except Exception as ex:
                print(ex)
            # проверка архитектуры
            finally:
                flag = True

                for index in tqdm(range(0, len(li))):
                    lin = li[index]
                    try:
                        if not os.path.exists(f"{project_name}\\{lin.split('/')[6]}"):  # model
                            os.mkdir(f"{project_name}\\{lin.split('/')[6]}")
                            if not os.path.exists(
                                    f"{project_name}\\{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}"):
                                os.mkdir(
                                    f"{project_name}\\{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}")
                            else:
                                continue
                            # https:// auto.ru/ cars/ used/ sale/ bentley/ continental_gt/ 1115616280-929f9ade/
                            os.mkdir(f"{project_name}\\{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}")
                            print("CREATE")
                            flag = True
                        else:
                            if not os.path.exists(
                                    f"{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}"):
                                os.mkdir(
                                    f"{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}")
                            else:
                                continue
                            # https:// auto.ru/ cars/ used/ sale/ bentley/ continental_gt/ 1115616280-929f9ade/
                            os.mkdir(f"{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}")
                            print("CREATE")
                        """os.mkdir(f"{project_name}/{names[index]}{count}")
                            flag = False"""
                    except Exception as ex:
                        #print(f"{YELLOW}PATH ALREADY EXIST or {ex}")
                        continue
                    # процесс скачивания
                    finally:
                        try:
                            temp = li[index]
                            try:
                                driver.get(temp)
                                print(f"{GREEN}LAUNCH CHROME{RESET}")
                            except Exception as ex:
                                print(ex)
                                driver.refresh()
                                print(f"{YELLOW}REFRESH{RESET}")
                            print(f"{GREEN}[+]WORK WITH {driver.current_url}{RESET}")

                            total_height = int(driver.execute_script("return document.body.scrollHeight") / 4)
                            print(f"{GREEN}[+]SCROLLING{RESET}")

                            pageHtml = driver.page_source
                            soupP = BeautifulSoup(pageHtml, "html.parser")
                            post_num = soupP.find('div', class_='CardHead__infoItem CardHead__id')

                            for i in range(3, total_height, 6):
                                driver.execute_script("window.scrollTo(0,{});".format(i))
                            for request in driver.requests:
                                if request.response:
                                    if request.url.split('/')[-1] == "1200x900n" and request.response.headers['Content-Type'] == 'image/webp':
                                        if request.url in already_loaded_img:
                                            continue
                                        else:
                                            already_loaded_img.append(request.url)
                                            webm_links_1200x900n.append(request.url)

                            """for request in driver.requests:
                                if request.response.headers['Content-Type'] == "image/webp" and request.url.split("/")[-1] == "1200x900n":
                                    webm_links_1200x900n.append(request.url)
                                    """
                            # if not fl:
                            print(
                                f"\r{GREEN}[+]HEADERS PARSED LOADING IMG FOR {project_name}\\{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}")
                            for imglink in tqdm(webm_links_1200x900n, colour="green"):
                                try:
                                    data = get_as_base64(imglink)
                                    imgdata = base64.b64decode(data)
                                    filename = f"{imglink.split('/')[-2]}.jpg"
                                    if flag:
                                        with open(f"{project_name}\\{lin.split('/')[6]}\\{lin.split('/')[7]}__{lin.split('/')[-2]}\\{filename}","wb") as f:
                                            f.write(imgdata)
                                    """else:
                                        with open(f"{project_name}/{names[index]}{count}/{filename}", "wb") as f:
                                            f.write(imgdata)"""
                                    """result = os.stat(f"images/{names[index]}{count}")
                                    if not result:
                                        os.rmdir(f"images/{names[index]}{count}")
                                        print(f"{YELLOW}DELETED : images/{names[index]}{count}{RESET}")"""

                                except Exception as ex:
                                    print(ex)
                                    print(f"{RED}[!]CANT LOAD IMG{RESET}")
                                    continue
                            #файл сохранения прогресса
                            with open(f"{project_name}\\complete.txt", "w") as s:
                                s.write(f"last:{temp} page:{page_int} links:{index}\\{len(li)}" + '\n')
                            webm_links_1200x900n.clear()

                        except Exception as ex:
                            print(ex)
                            print(f"{RED}CANT OPEN {driver.current_url}{RESET}")
                            # continue for 3.10

                        #print(f"{GREEN}[*] THAT'S ALL {RESET} last:{temp} page:{page_int} links:{index}/{len(li)} {RESET}" + '\n')
            li.clear()
            webm_links_1200x900n.clear()
            already_loaded_img.clear()
            page_int = 1
            links_clear.clear()
    except Exception as ex:
        print(ex)


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
# nice detection
# az/11030162 truck 254 126 1303 1019 : 0.63 ; person 684 357 800 453 0.007


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
    toc = time.perf_counter()
    print(f"Вычисление заняло {toc - tic:0.4f} секунд")


if __name__ == "__main__":
    import argparse



    parser = argparse.ArgumentParser(description="Pre-release AVparser v0.3 with Python 3.9.7")
    parser.add_argument("-p", "--parser",  help="Parser avto.ru. recommended format https://link/?year", action="store_true")
    parser.add_argument("-f", "--imageai_filter", help="imageai light filtering image from trash (only cars as possible)", default=80, action="store_true")
    parser.add_argument("-c", "--cpu_cores", help="(SOON)count of usage cpu cores for imageai recommended cpu_count() / 2", default=2, action="store_true")

    execution_path = os.getcwd()
    images_list = []
    src = execution_path + "\\src"
    output = execution_path + "\\output"
    #detected = execution_path + "\\detect"

    args = parser.parse_args()
    if args.parser:
        print(f"{GREEN}[+] START PARSER{RESET}")
        try:
            if not os.path.exists("src"):
                os.mkdir("src")
                print(f"{GREEN}[+] src created{RESET}")
            if not os.path.exists("output"):
                os.mkdir("output")
                print(f"{GREEN}[+] output created{RESET}")
            if not os.path.exists("model"):
                os.mkdir("model")
                print(f"{GREEN}[+] model created{RESET}")
        except Exception as ex:
            print(ex)

        main_parser(src)
    elif args.imageai_filter:
        ############
        print(f"{GREEN}[+] START FILTER {RESET}")

        try:
            if not os.path.exists("src"):
                os.mkdir("src")
                print(f"{GREEN}[+] src created{RESET}")
            if not os.path.exists("output"):
                os.mkdir("output")
                print(f"{GREEN}[+] output created{RESET}")
            if not os.path.exists("model"):
                os.mkdir("model")
                print(f"{GREEN}[+] model created{RESET}")
        except Exception as ex:
            print(ex)

        pic_folders = os.listdir(src)
        tic = time.perf_counter()
        projects_folder = os.listdir(src)
        print("[+] pic scanning")

        proj_folders = []
        models_folders = []
        models = []
        src_path = execution_path + "\\src"
        src_folders = os.listdir(src_path)

        try:
            for project in src_folders:
                project_path = src_path + "\\" + project
                if not os.path.exists(output + '\\' + project):
                    os.mkdir(output + '\\' + project)
                models = os.listdir(project_path)
                for model in models:
                    try:
                        if model == "complete.txt" or model == "fetched.txt":
                            continue
                        else:
                            model_path = project_path + '\\' + model
                            if not os.path.exists(output + '\\' + project + '\\' + model):
                                os.mkdir(output + '\\' + project + '\\' + model)
                            print("\t", model_path)
                            orders = os.listdir(model_path)
                            for i in orders:
                                orders_path = project_path + '\\' + model + '\\' + i
                                if not os.path.exists(output + '\\' + project + '\\' + model + '\\' + i):
                                    os.mkdir(output + '\\' + project + '\\' + model + '\\' + i)
                                print('\t\t', orders_path)
                                images = os.listdir(orders_path)
                                for image in images:
                                    image_path = orders_path + '\\' + image
                                    images_list.append(image_path)
                                    print("\t\t\t", image_path)
                    except Exception as ex:
                        print(f"{RED}[!]main probably dont get under dir \output\projects\models\:{ex}{RESET}")
                        time.sleep(5)
        except Exception as ex:
            print(ex)
        master(images_list)
    else:
        print("[?]NO PARAMS: main.py -h")