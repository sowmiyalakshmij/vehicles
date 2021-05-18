FROM python:3.6

COPY ./requirements.txt /
COPY ./setupMongo.py /

RUN pip3 install --upgrade pip==20.2.4
RUN pip3 install -r ./requirements.txt
#RUN python setupMongo.py

WORKDIR /server/vehicles
COPY ./server/vehicles /server/vehicles

ENV PYTHONPATH="/:/server/:/server/vehicles:/server/vehicles/api"
ENV FLASK_APP="vehiclesApp"
ENV FLASK_ENV="development"

EXPOSE 5000

WORKDIR /


CMD ["flask", "run", "--host", "0.0.0.0"]

