FROM python:3.10

COPY . .

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
RUN pip install yt-dlp