import requests
import base64
from PIL import Image

# URL of your local API
url = "http://127.0.0.1:8000/ocr/bbox-to-text/"

# Path to your test image
image_path = "app/images/ingredients-1.png"

# Read the image and encode it to base64
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# Get image dimensions
with Image.open(image_path) as img:
    width, height = img.size

# Prepare the payload
payload = {
    "image": encoded_string,
    "x": 0,
    "y": 0,
    "width": width,
    "height": height
}

# Send POST request
response = requests.post(url, json=payload)

# Print the response
print(response.status_code)
print(response.json())

"""
usage: python test_ocr_api.py
"""