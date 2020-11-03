import pyqrcode
import sys

# Create
url = pyqrcode.create('http://127.0.0.1:8000/')
url.svg("/Users/elizabeth/restaurants/qr.svg", scale=6, module_color="#000000")
