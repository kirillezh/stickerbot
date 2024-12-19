FROM python:3.10-slim

#install ffmpeg
RUN apt-get -y update
RUN apt-get install -y ffmpeg

COPY . .
RUN pip install --upgrade pip; \
    pip install -r requirements.txt

ENV DISPLAY=:99
ENV APP_HOME /program 

#set workspace
WORKDIR ${APP_HOME}

ENTRYPOINT ["python3"]

CMD ["main.py"]