import shutil
import time
import io
import base64
import requests
from fastapi.testclient import TestClient
from PIL import Image, ImageChops
from app.main import app
from app.core.config import BASE_DIR, UPLOAD_DIR, get_settings

client = TestClient(app)

"""
Test cases for endpoint "/"
"""
def test_get_home():
    response = client.get("/") # requests.get("") # python requests
    #assert response.text != "<h1>Hello world</h1>"
    assert response.status_code == 200
    assert  "text/html" in response.headers['content-type']


def test_prediction_upload_missing_headers():
    img_saved_path = BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/",
            files={"file": open(path, 'rb')}
        )
        assert response.status_code == 401


def test_prediction_upload():
    img_saved_path = BASE_DIR / "images"
    settings = get_settings()
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/",
            files={"file": open(path, 'rb')},
            headers={"Authorization": f"JWT {settings.app_auth_token}"}
        )
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            data = response.json()
            assert len(data.keys()) == 2


def test_echo_upload():
    img_saved_path = BASE_DIR / "images"
    for path in img_saved_path.glob("*"):
        try:
            img = Image.open(path)
        except:
            img = None
        response = client.post("/img-echo/", files={"file": open(path, 'rb')})
        if img is None:
            assert response.status_code == 400
        else:
            # Returning a valid image
            assert response.status_code == 200
            r_stream = io.BytesIO(response.content)
            echo_img = Image.open(r_stream)
            difference = ImageChops.difference(echo_img, img).getbbox()
            assert difference is None
    # time.sleep(3)
    #shutil.rmtree(UPLOAD_DIR)        
    # 

"""
Test cases for api endpoint "/ocr/bbox-to-text/"
"""
# URL of your local API
url_bbox_to_text = "/ocr/bbox-to-text/"

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
response = client.post(url_bbox_to_text, json=payload)



"""
Test cases for api endpoint /ocr/upload_file
"""
url_upload_file = "/ocr/upload-file/"
def test_upload_file_success():
    # Test with a valid image file
    test_image_path = BASE_DIR / "app" / "images" / "ingredients-1.png"

    with open(test_image_path, "rb") as image_file:
        #response = client.post("/ocr/encoding-file/", files={"file": (image_file, "image/png")})
        response = client.post(url_upload_file, files={"file": ("image.png", image_file, "image/png")})

    assert response.status_code == 200
    data = response.json()

    assert "image" in data
    assert "x" in data
    assert "y" in data
    assert "width" in data
    assert "height" in data

    assert data["x"] == 0
    assert data["y"] == 0

    # Verify the image dimensions
    with Image.open(test_image_path) as img:
        assert data["width"] == img.width
        assert data["height"] == img.height

    # Verify the base64 encoded image
    decoded_image = base64.b64decode(data["image"])
    img = Image.open(io.BytesIO(decoded_image))
    assert img.format.lower() in ['png', 'jpeg']

def test_upload_file_invalid_file():
    # Test with an invalid file (not an image)
    with open(__file__, "rb") as text_file:
        response = client.post(url_upload_file, files={"file": ("test.txt", text_file, "text/plain")})

    # Check if the response contains an error message
    response_json = response.json()
    assert any('Invalid' in str(value) for value in response_json.values()), "Expected an 'Invalid' error message in the response"

def test_upload_file_no_file():
    # Test without uploading any file
    response = client.post(url_upload_file)

    assert response.status_code == 422  # Unprocessable Entity

def test_upload_file_large_image():
    # Create a large image for testing
    large_image = Image.new('RGB', (5000, 5000))
    img_byte_arr = io.BytesIO()
    large_image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    response = client.post(url_upload_file, files={"file": ("large_image.png", img_byte_arr, "image/png")})

    assert response.status_code == 200
    data = response.json()
    assert data["width"] == 5000
    assert data["height"] == 5000

def test_upload_file_different_formats():
    formats = ['PNG', 'JPEG', 'GIF']
    for fmt in formats:
        img = Image.new('RGB', (100, 100))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=fmt)
        img_byte_arr = img_byte_arr.getvalue()

        response = client.post(url_upload_file, files={"file": (f"test_image.{fmt.lower()}", img_byte_arr, f"image/{fmt.lower()}")})

        assert response.status_code == 200
        data = response.json()
        assert data["width"] == 100
        assert data["height"] == 100    #   