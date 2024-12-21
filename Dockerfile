FROM python:3.13.1-alpine

# Install ffmpeg
RUN apk add --no-cache ffmpeg

COPY requirements.txt .
RUN pip install --upgrade pip; \
    pip install -r requirements.txt

ENV DISPLAY=:99
ENV APP_HOME=/program

# Set workspace
WORKDIR ${APP_HOME}

ENTRYPOINT ["python3"]

CMD ["main.py"]