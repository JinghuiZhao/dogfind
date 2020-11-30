FROM python:3.7

ADD ./app /home/app/
ADD requirements.txt /home/app/

ENV HOSTNAME db
ENV USERNAME elainezhao
ENV DB_PASSWORD zjh611611
ENV DATABASE_NAME flask_app
ENV DB_PORT 5432

ENV TABLE_PATH data/final_latest.csv
ENV VECTOR_PATH data/efficientnet_embeddings.out

# ENV VECTOR_PATH data/inception_embeddings.out

WORKDIR /home/app/
RUN pip3 install -r requirements.txt 

EXPOSE 5000
ENTRYPOINT ["python3", "app.py"]