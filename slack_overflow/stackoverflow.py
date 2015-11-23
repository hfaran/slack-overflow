import re
from urlparse import urlparse

from stackexchange import Site
from stackexchange import Question

from slack_overflow.google_search import search


_question_regex = re.compile('^/questions/(\d+)/')


def _get_question_nid(match):
    """Returns the Question ID given a match from the URL

    :rtype: int|None
    """
    if match is None:
        return None
    return int(match.groups()[0])


def extract_question_nid_from_url(url):
    """Extracts the ID of the question from the provided stackoverflow URL

    :type url: str
    :rtype: int
    """
    purl = urlparse(url)
    assert purl.netloc.endswith('stackoverflow.com'), \
        "Non-StackOverflow result {}; search is broken!"\
        .format(url)
    qnid = _get_question_nid(_question_regex.match(purl.path))
    return qnid


def google_search_stackoverflow_query(query, pages=1):
    """Returns google's result for the query in stackoverflow questions

    :rtype: list
    """
    return search(
        "site:stackoverflow.com/questions/* {}".format(query),
        pages=pages
    )


def get_question_top_answer_body(so, question):
    """Returns body of the most upvoted answer in question

    :type so: Site
    :type question: Question
    :rtype: str|None
    """
    if not question.answers:
        return None
    top_answer = sorted(question.answers,
                        key=lambda a: a.score, reverse=True)[0]
    body = so.answer(top_answer.id, body=True).body
    return body
