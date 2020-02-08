FROM alpine:latest
RUN apk --update-cache add git python3
RUN pip3 install --upgrade pip
RUN git clone https://github.com/kumarstack55/python-json-formatter.git
RUN pip install -r ./python-json-formatter/requirements.txt
CMD python3 ./python-json-formatter/app.py -p 80
