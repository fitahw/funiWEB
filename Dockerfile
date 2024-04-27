FROM python:3.10

COPY . .

RUN apt-get install ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
