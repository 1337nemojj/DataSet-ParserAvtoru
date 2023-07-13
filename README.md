# AvtoMarks DataSet Creator for training autoClassificator or smth... 

> images parser for avto.ru and filtering them for dataset. 
This programm is Kursovaya dont use it for Kursovaya in own case.
## INSTALLATION:
### Prepairing:
*  ```python -m venv venv```
* ```/venv/Scpits/activate.bat``` - for Win 

### Requrements for Selenium ```python main.py -p```:
* selenium-wire
* selenium
* chromedriver_autoinstaller
### Requrements openCV + yolov3 ```python main.py -f``` (openCV+yolov3 used instead of imageai):


put in model's files in path like this: 

```~/model/coco.names```
```~/model/yolov3.cfg```
```~/model/yolov3.weights```

## USAGE:
## Parser only
1. activate venv
2. launch ```python main.py -p``` -> choose setup for searching cars on avto.ru in filters

3. enter link(s) with "Enter" ex.```https://auto.ru/sankt-peterburg/cars/bmw/all/?year_to=2022&price_from=8000000``` and press 2nd "Enter" for confirm
4. name project -> it's create new dir for data
5. that's launch automated browser and parse images 

## OpenCV filter
1. launch ```python main.py -f```
2. all images from path src will be filtered and valid images be copied to ```/ouput/``` path

## Parser + filtering

```python main.py```

