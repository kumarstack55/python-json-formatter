#!/usr/bin/env python
# coding: utf-8

import flask
import html
import jinja2
import json


app = flask.Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    ctx = dict()
    if flask.request.method == 'POST':
        json_text = flask.request.form["in"]

        ctx['in'] = html.escape(json_text)

        try:
            data = json.loads(json_text)
            ctx['out'] = html.escape(
                    json.dumps(data, sort_keys=True, indent=2))
        except json.decoder.JSONDecodeError as e:
            ctx['out'] = html.escape(str(e))

    env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
    template = env.get_template('index.html.j2')
    return template.render(ctx)


if __name__ == '__main__':
    debug = False
    app.run(debug=debug)
