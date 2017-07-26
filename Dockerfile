# our base image
# FROM tensorflow/tensorflow
FROM python:3-onbuild


# specify the port number the container should expose
EXPOSE 5000

COPY flask-ml /flask-ml

WORKDIR /flask-ml

RUN pip --no-cache-dir install flask
RUN pip --no-cache-dir install tensorflow
# RUN pip --no-cache-dir install -r requirements.txt

# run the application
CMD ["python", "app.py"]
