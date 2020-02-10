FROM alpine:latest
ADD . /python-json-formatter
WORKDIR /python-json-formatter
RUN set -x && apk --update-cache add python3
RUN set -x \
  && pip3 install --upgrade pip \
  && pip3 install -r requirements.txt
CMD ["python3" "./app.py", "-p", "80"]
EXPOSE 80
