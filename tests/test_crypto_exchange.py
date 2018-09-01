#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `crypto_exchange` package."""

import pytest


from crypto_exchange import crypto_exchange


class A(object):

    def __radd__(self, other):
        pass

    def __init__(self):

        pass

    def __xxx(self):
        pass


    def _ab(self):
        pass



@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
