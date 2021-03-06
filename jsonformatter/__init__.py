#!/usr/bin/env python3
from flask import Flask
import argparse
import flask
import jinja2
import json
import pathlib
import wtforms


JSON_SAMPLE = '''\
{ "menu": { "id": "file", "value": "File", "popup": {
"menuitem": [ {"value": "New", "onclick": "CreateNewDoc()"},
{"value": "Open", "onclick": "OpenDoc()"}, {"value": "Close",
"onclick": "CloseDoc()"} ] } } }
'''


class Form(wtforms.Form):
    enable_sort_keys = wtforms.BooleanField(
            "enable_sort_keys", default=False)
    enable_indent = wtforms.BooleanField(
            "enable_indent", default="checked")
    enable_compact = wtforms.BooleanField("enable_compact")
    indent_width = wtforms.SelectField(
            "indent_width",
            choices=[(2, "2"), (4, "4"), (8, "8")],
            default=2, coerce=int)
    enable_json_only = wtforms.BooleanField(
            "enable_json_only", default=False)
    input_json = wtforms.TextAreaField(
            "input_json", default=JSON_SAMPLE)
    output_json = wtforms.TextAreaField("output_json")


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if flask.request.method == "POST":
            form = Form(flask.request.form)
        else:
            form = Form()

        indent = None
        if form.enable_indent.data:
            indent = form.indent_width.data

        separators = None
        if form.enable_compact.data:
            separators = (',', ':')

        try:
            form.output_json.data = json.dumps(
                    json.loads(form.input_json.data),
                    sort_keys=form.enable_sort_keys.data,
                    separators=separators,
                    indent=indent)
            if form.enable_json_only.data:
                return flask.Response(
                    form.output_json.data,
                    mimetype="application/json; charset=utf-8")
        except json.decoder.JSONDecodeError as e:
            if form.enable_json_only.data:
                flask.abort(400)
            form.output_json.data = str(e)

        templates_dir = \
            pathlib.Path(__file__).resolve().parent \
            / "templates"
        loader = jinja2.FileSystemLoader(templates_dir)
        env = jinja2.Environment(loader=loader)
        template = env.get_template("index.html.j2")
        ctx = dict(form=form)
        return template.render(ctx)

    return app


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--port', default=5000)
    args = parser.parse_args()

    app = create_app()
    app.run(host='0.0.0.0', port=args.port)
