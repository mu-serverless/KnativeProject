FROM python:latest
RUN apt update
RUN apt install -y python3-pip
ADD ./requirements.txt /server/
RUN pip3 install -r /server/requirements.txt
ADD server.py /server/
WORKDIR /server/
EXPOSE 8080

CMD [ "python3", "/server/server.py" ]


