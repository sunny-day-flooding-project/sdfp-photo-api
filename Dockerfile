FROM python:3.10.4

WORKDIR /code

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 libimage-exiftool-perl -y

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV PYTHONUNBUFFERED=1

EXPOSE 5432

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "app/log_conf.yaml"]
