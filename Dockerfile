FROM python:3.8-slim
MAINTAINER Sonu Prasad

WORKDIR /app
ADD . /app

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/app/us_data_downloader.py"]