FROM osgeo/gdal

ENV DEBIAN_FRONTEND noninteractive

USER root

RUN mkdir -p /usr/src/process

RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt-get install python3.9 -y

COPY ./process.py /usr/src/process