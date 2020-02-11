#!/usr/bin/env python3
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


app = flask.Flask(__name__)


class Form(wtforms.Form):
    enable_sort_keys = wtforms.BooleanField(
            "enable_sort_keys", default=False)
    enable_indent = wtforms.BooleanField(
            "enable_indent", default="checked")
    enable_compact = wtforms.BooleanField("enable_compact")
    indent_width = wtforms.SelectField(
            "indent_width", choices=[(2, "2"), (4, "4"), (8, "8")],
            default=2, coerce=int)
    enable_json_only = wtforms.BooleanField(
            "enable_json_only", default=False)
    input_json = wtforms.TextAreaField(
            "input_json", default=JSON_SAMPLE)
    output_json = wtforms.TextAreaField("output_json")


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

    script_dir = pathlib.Path(__file__).resolve().parent.parent
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(script_dir))
    template = env.get_template("index.html.j2")
    ctx = dict(form=form)
    return template.render(ctx)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", "-p", type=int, default=5000)
    parser.add_argument("--debug", action="store_true", default=False)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)
