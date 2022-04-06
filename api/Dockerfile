# Start from a python image
FROM python:3.10-alpine

# Create a new directory to allocate our API
WORKDIR /omegaterapia_api

# Copy requirements and install
COPY requirements.txt /omegaterapia_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /omegaterapia_api/requirements.txt

# Copy API project
COPY app /omegaterapia_api/app

# Run uvicorn server with our API on port 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]