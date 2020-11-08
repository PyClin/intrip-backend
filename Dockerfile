FROM python:3.7
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /config/
RUN pip install -r /config/requirements.txt
COPY ./src/ /code/