# Start from a python image
FROM python:3.10-alpine

# Create a new directory to allocate our API
WORKDIR /omegaterapia_api

# Prepare requirements
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

# Copy requirements and install
COPY requirements.txt /omegaterapia_api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /omegaterapia_api/requirements.txt

# Clear
RUN  apk --purge del .build-deps

# Copy API project
COPY app /omegaterapia_api/app

# Run uvicorn server with our API on port 80
CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0"]