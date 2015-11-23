import re
from urlparse import urlparse

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
    return search(
        "site:stackoverflow.com/questions/* {}".format(query),
        pages=pages
    )
