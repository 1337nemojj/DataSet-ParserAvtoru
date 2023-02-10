import base64
import requests

def get_as_base64(url):
    return base64.b64encode(requests.get(url).content)
