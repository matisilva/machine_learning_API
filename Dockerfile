FROM python:3.5-slim
ADD requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir src
WORKDIR src
ADD . .