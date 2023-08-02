FROM python:3.11-bookworm

RUN mkdir /webparser
WORKDIR /webparser
ADD . /webparser
COPY requirements.txt /webparser/
RUN pip install -r requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt -y upgrade
RUN apt -y install default-jdk
RUN rm -rf /var/lib/apt/lists/*
COPY . /webparser/