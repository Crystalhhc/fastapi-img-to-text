FROM python:3.10

WORKDIR /app


# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy ./app/custom_tessdata/*.* to /user/share/local/tesseract directory
RUN mkdir -p /usr/share/tessdata 
COPY  ./app/custom_tessdata/*.*  /user/local/share/tessdata/
   
# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]