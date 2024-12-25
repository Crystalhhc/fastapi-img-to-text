## Run
```bash
% uvicorn app.main:app --reload
```
## Docker Hub
```bash
% docker build -t crystalchen/fastapi-img-to-text .
docker tag crystalchen/fastapi-img-to-text:latest crystalchen/fastapi-img-to-text:latest
docker push crystalchen/fastapi-img-to-text:latest
```

## Directory Structure
```
fastapi-img-to-text/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           └── ocr.py
│   ├── core/
│   │   └── config.py
│   └── main.py
└── templates/
    └── home.html
```

## Enable Traditional Chinese Character Recognition
Step1: To get the latest version of the `chi_tra.traineddata` and save it to `./app/custom_tessdata/`
Step2: copy `chi_tra.traineddata` to `/usr/local/share/tessdata/`
```zsh
cp ./app/custom_tessdata/chi_tra.traineddata /usr/local/share/tessdata/
```
Step3: Check Tesseract has acknowledged this version
```zsh
tesseract --list-langs
List of available languages in "/usr/local/share/tessdata/" (4):
chi_tra
eng
osd
snum
```
Step4: Update the Python environment:
Make sure that the pytesseract library installed in the Python environment. It's already listed in your requirements.txt, but if you haven't installed it yet,

Step5: Update the Code
```python
import pytesseract
from PIL import Image

# Load an image
image = Image.open('path_to_your_image.png')``
custome_config = r'--oem 3 --psm 6' # It is needed.
text = pytesseract.image_to_string(img, config=custome_config, lang='chi_tra')
```