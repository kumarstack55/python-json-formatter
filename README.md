# python-json-formatter

## requirements

* Python 3

## build

```bash
git clone https://github.com/kumarstack55/python-json-formatter.git
cd python-json-formatter

sudo docker build -t python-json-formatter ./
sudo docker run --name python-json-formatter -d -p 80:80 python-json-formatter

curl http://127.0.0.1/
```

## test

```bash
PYTHONPATH=./src pytest -s
```