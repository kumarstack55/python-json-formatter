FROM alpine:latest
COPY ./ /src
WORKDIR /src
RUN set -x \
  && apk --update-cache add python3 \
  && pip3 install --upgrade pip \
  && pip3 install -e .
CMD ["python3", "jsonformatter/__init__.py"]
EXPOSE 5000
