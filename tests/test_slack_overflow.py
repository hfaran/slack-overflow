import unittest
from collections import namedtuple

import flask
from mock import Mock
from mock import patch

import slack_overflow


class TestSlackOverflow(unittest.TestCase):
    def setUp(self):
        slack_overflow.app.config['TESTING'] = True
        self.app = slack_overflow.app.test_client()

    def tearDown(self):
        pass

    # @patch('slack_overflow.google_search_stackoverflow_query')
    # def test_overflow(self, google_search_stackoverflow_query):
    #     google_search_stackoverflow_query = Mock()
    #     Question = namedtuple('Question', ['id', 'score'])
    #     questions = [Question(1, 1), Question(2, 2)]
    #     so = Mock()
    #
    #     top = flask._app_ctx_stack
    #     top.so = so
    #     top.max_questions = 10
    #
    #     rv = self.app.post('/soi', data={"text": "foobar"})
    #     print(rv)

    # TODO just test each route with live web use for now?
