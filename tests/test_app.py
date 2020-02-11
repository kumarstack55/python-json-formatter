#!/usr/bin/env python
# coding: utf-8

import os
import tempfile
import pytest

from jsonformatter import app as jfapp


@pytest.fixture
def client():
    jfapp.app.config['TESTING'] = True
    with jfapp.app.test_client() as client:
        yield client

def test_index_get(client):
    rv = client.get('/')
    assert b'<title>JSON Formatter</title>' in rv.data

def test_index_post_json_only(client):
    data = dict(
        enable_json_only='y',
        input_json='{"b":2, "a":1}'
    )
    rv = client.post('/', data=data)
    assert b'{"b": 2, "a": 1}' in rv.data

def test_index_post_sort_keys(client):
    data = dict(
        enable_json_only='y',
        enable_sort_keys='y',
        input_json='{"b":2, "a":1}'
    )
    rv = client.post('/', data=data)
    assert b'{"a": 1, "b": 2}' in rv.data
