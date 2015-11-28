import sys; sys.path.append(".")

from collections import namedtuple

from mock import Mock

from slack_overflow.stackoverflow import _get_question_nid
from slack_overflow.stackoverflow import extract_question_nid_from_url
from slack_overflow.stackoverflow import get_question_top_answer_body


def test___get_question_nid__no_match():
    assert _get_question_nid(None) is None


def test___get_question_nid__match():
    match = Mock()
    match.groups.return_value = ("56743",)
    assert _get_question_nid(match) == 56743


def test__extract_question_nid_from_url__exists():
    url = "https://stackoverflow.com/questions/5341006/" \
          "where-should-i-put-tests-when-packaging-python-modules"
    assert extract_question_nid_from_url(url) == 5341006


def test__extract_question_nid_from_url__None():
    url = "https://stackoverflow.com/questions/tagged/python"
    assert extract_question_nid_from_url(url) is None


def test__get_question_top_answer_body__no_answers():
    so = Mock()
    question = Mock()
    question.answers = []
    assert get_question_top_answer_body(so, question) is None


def test__get_question_top_answer_body__answers():
    Answer = namedtuple('Answer', ['id', 'score'])
    answers = [Answer(1, 1), Answer(2, 2)]

    so = Mock()
    fetched_answer = Mock()
    fetched_answer.body = "foobar"
    so.answer.return_value = fetched_answer
    question = Mock()
    question.answers = answers
    assert get_question_top_answer_body(so, question) == "foobar"
