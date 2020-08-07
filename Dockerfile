FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY . /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app/code/app
RUN . ../../env/test_env.sh

ENTRYPOINT [ "python3" ]
CMD ["app.py"]