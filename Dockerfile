FROM python:3.10

COPY . .

RUN apt-get install ffmpeg && pip install --no-cache-dir -r requirements.txt

CMD ["python", "funi.py"]
