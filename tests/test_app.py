#!/usr/bin/env python
# coding: utf-8

import os
import tempfile
import pytest

import jsonformatter as jf


@pytest.fixture
def client():
    app = jf.create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    rv = client.get('/')
    assert b'<title>JSON Formatter</title>' in rv.data

def test_index_post(client):
    data = dict(
        input_json='{"b":2, "a":1}'
    )
    rv = client.post('/', data=data)
    assert b'<title>JSON Formatter</title>' in rv.data

def test_output_msg_when_invalid_json_is_given(client):
    data = dict(
        input_json='{'
    )
    rv = client.post('/', data=data)
    assert b'Expecting property name enclosed in double quotes' in rv.data

def test_do_not_include_html_in_output(client):
    data = dict(
        input_json='["<s>test</s>"]'
    )
    rv = client.post('/', data=data)
    assert b'<s>test</s>' not in rv.data

def test_enable_json_only(client):
    data = dict(
        enable_json_only='y',
        input_json='{"b":2, "a":1}'
    )
    rv = client.post('/', data=data)
    assert b'{"b": 2, "a": 1}' in rv.data

def test_returns_bad_gateway_if_invalid_json_is_given(client):
    data = dict(
        enable_json_only='y',
        input_json='{'
    )
    rv = client.post('/', data=data)
    assert rv.status_code == 400

def test_enable_compact(client):
    data = dict(
        enable_json_only='y',
        enable_compact='y',
        input_json='{"b":2, "a":1}'
    )
    rv = client.post('/', data=data)
    assert b'{"b":2,"a":1}' in rv.data

def test_enable_sort_keys(client):
    data = dict(
        enable_json_only='y',
        enable_compact='y',
        enable_sort_keys='y',
        input_json='{"b":2, "a":1}'
    )
    rv = client.post('/', data=data)
    assert b'{"a":1,"b":2}' in rv.data
