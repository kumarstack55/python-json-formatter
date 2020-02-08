#!/usr/bin/env python
# coding: utf-8

import flask
import html
import jinja2
import json
import argparse


SORT_KEYS_DEFAULT = False
INDENT_DEFAULT = 2
JSON_SAMPLE = '''
{ "menu": { "id": "file", "value": "File", "popup": {
"menuitem": [ {"value": "New", "onclick": "CreateNewDoc()"},
{"value": "Open", "onclick": "OpenDoc()"}, {"value": "Close",
"onclick": "CloseDoc()"} ] } } }
'''


app = flask.Flask(__name__)


def form_to_bool(raw_value: str) -> bool:
    return raw_value == 't'


def form_to_int(raw_value: str) -> bool:
    if raw_value == 'None':
        return None
    return int(raw_value)


def get_indent_items(indent) -> list:
    indent_items = []
    for v in ['None', 2, 4]:
        item = dict()

        item['value'] = v

        item['selected'] = ''
        if v == indent:
            item['selected'] = ' selected'

        item['text'] = v
        if v == 'None':
            item['text'] = 'Compact'

        indent_items.append(item)
    return indent_items


def get_body(method: str, form: dict) -> str:
    ctx = dict()

    json_text_raw = JSON_SAMPLE
    if method == 'POST':
        json_text_raw = form['in']

    ctx['sort_keys'] = SORT_KEYS_DEFAULT
    if method == 'POST':
        ctx['sort_keys'] = \
                form_to_bool(form.get('sort_keys', 'f'))

    ctx['indent'] = INDENT_DEFAULT
    if method == 'POST':
        ctx['indent'] = form_to_int(form['indent'])

    ctx['in'] = html.escape(json_text_raw)

    try:
        data = json.loads(json_text_raw)
        ctx['out'] = html.escape(
                json.dumps(
                    data, sort_keys=ctx.get('sort_keys'),
                    indent=ctx.get('indent')))
    except json.decoder.JSONDecodeError as e:
        ctx['out'] = html.escape(str(e))

    ctx['indent_items'] = get_indent_items(ctx['indent'])

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template('index.html.j2')
    return template.render(ctx)


@app.route('/', methods=['GET', 'POST'])
def index():
    return get_body(flask.request.method, flask.request.form)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', '-p', type=int, default=5000)
    parser.add_argument('--debug', action='store_true', default=False)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=debug)
