# AvtoMarks DataSet Creator for training autoClassificator or smth... 

> images parser for avto.ru and filtering them for dataset. 
This programm is Kursovaya dont use it for Kursovaya in own case.
## Installation
### Prepairing:
1. ```python -m venv venv```
2. ```/venv/Scpits/activate.bat``` - for Win 
3. ```pip install -r requirements.txt```
### Requrements for Selenium ```python main.py -p```:
All requirements should be installed by ```pip install -r requirements.txt``` (but not sure)
### Requrements for imageai ```python main.py -f``` (not working atm):
 all librares from docs IMAGEAI

1. ``` pip install cython pillow>=7.0.0 numpy>=1.18.1 opencv-python>=4.1.2 torch>=1.9.0 --extra-index-url https://download.pytorch.org/whl/cu102 torchvision>=0.10.0 --extra-index-url https://download.pytorch.org/whl/cu102 pytest==7.1.3 tqdm==4.64.1 scipy>=1.7.3 matplotlib>=3.4.3 mock==4.0.3```
2. ```pip install imageai --upgrade```

 model for example in ImageAi docs:
https://imageai.readthedocs.io/en/latest/detection/index.html 

link (Download link): ```https://github.com/OlafenwaMoses/ImageAI/releases/download/3.0.0-pretrained/yolov3.pt/```

put in model in path like this: ```~/model/yolov3.pt```

(not working atm)
