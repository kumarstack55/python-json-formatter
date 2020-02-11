FROM alpine:latest
COPY ./src /src
WORKDIR /src
RUN set -x \
  && apk --update-cache add python3 \
  && pip3 install --upgrade pip \
  && pip3 install -r requirements.txt
CMD ["python3", "./jsonformatter/app.py", "-p", "80"]
EXPOSE 80
