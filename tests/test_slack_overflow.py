import json
import unittest

import flask
from stackexchange import StackOverflow, Site

import slack_overflow


def live_test(fn):
    """Decorate a test with this that uses live testing"""
    def _test(*args, **kwargs):
        so = Site(domain=StackOverflow)
        top = flask._app_ctx_stack
        top.so = so
        top.max_questions = 5

        return fn(*args, **kwargs)
    return _test


class TestSlackOverflowFunctional(unittest.TestCase):
    """Functional test for the application"""
    def setUp(self):
        slack_overflow.app.config['TESTING'] = True
        self.app = slack_overflow.app.test_client()

    def tearDown(self):
        pass

    @live_test
    def test__overflow__success(self):
        """This is a live test that goes against SO and Google

        Live tests here make sense, because if these tests do not
        pass, it is likely that the app in effect on Slack is not
        performing as it should.
        """
        rv = self.app.post('/overflow', data={"text": "foobar"})
        print(rv.data)
        assert any(any(
            term in line for line in rv.data.splitlines()
            if "stackoverflow.com" in line
        ) for term in ("foo", "bar"))

    @live_test
    def test__overflow__no_questions(self):
        rv = self.app.post(
            '/overflow',
            data={"text": "87up98dhyfuqhwefuqh;wpeoufhqp;wdjnf;q"}
        )
        print(rv.data)
        assert "No questions for the given query were found!" in rv.data

    @live_test
    def test__soi__success(self):
        """This is a live test that goes against SO and Google"""
        rv = self.app.post('/soi', data={"text": "parse xhtml with regex"})
        print(rv.data)
        assert "Have you tried using an XML parser instead?" in rv.data

    @live_test
    def test__soi__no_questions(self):
        rv = self.app.post(
            '/soi',
            data={"text": "87up98dhyfuqhwefuqh;wpeoufhqp;wdjnf;q"}
        )
        print(rv.data)
        assert "No questions for the given query were found!" in rv.data

    def test__root(self):
        rv = self.app.get('/')
        print(rv.data)
        assert all(term in rv.data for term in ("Redirecting", "github"))

    def test__version(self):
        rv = self.app.get('/version')
        print(rv.data)
        assert json.loads(rv.data)["version"] == slack_overflow.__version__
