FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

ADD ./app /home/app/
ADD requirements.txt /home/app/

WORKDIR /home/app/


RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]