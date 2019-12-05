FROM python:3.7
EXPOSE 5000

# CMD mkdir /app
#WORKDIR /app

WORKDIR /app


#COPY . /app
#
#ENV FLASK_APP run.py
#ENV FLASK_RUN_HOST 0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers
#RUN pip install -r requirements.txt
#
#ENTRYPOINT [ "py

#RUN apt-get update -y && \
#    apt-get install -y python-pip python-dev
ADD config_default.py /app
# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt



RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]