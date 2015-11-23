import logging
import re
from urlparse import urlparse

import flask
from flask import Flask, request, Response, redirect

from slack_overflow.google_search import search


app = Flask(__name__)


############
# Handlers #
############

@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow python list comprehension
    '''
    question_regex = re.compile('^/questions/(\d+)/')

    def get_question_nid(match):
        """Returns the Question ID given a match from the URL"""
        if match is None:
            return None
        return int(match.groups()[0])

    # Get objects on the application context pushed on startup
    max_questions = flask._app_ctx_stack.max_questions
    so = flask._app_ctx_stack.so
    # Each page in the google search has ten entries
    pages = max_questions//10 + 1

    text = request.values.get('text')

    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    # Perform google search
    #  Filter searches for only questions, and "-tagged" removes
    #   /questions/tagged entries for us, which should leave actual
    #   question links for most results
    sr = search(
        "site:stackoverflow.com/questions/* -tagged {}".format(text),
        pages=pages
    )
    # Extract each question nid from results
    so_qnids = []
    for result in sr:
        purl = urlparse(result.link)
        assert purl.netloc == 'stackoverflow.com', \
            "Non-StackOverflow result {}; search is broken!"\
            .format(result.link)
        qnid = get_question_nid(question_regex.match(purl.path))
        if qnid is not None:
            so_qnids.append(qnid)
        else:
            logging.warning("Found invalid URL in search: "
                            "{}".format(result.link))
    # Fetch Questions using SO API
    so_qs = so.questions(so_qnids)
    # Sort Questions by score
    so_qs = sorted(so_qs, key=lambda q: q.score, reverse=True)
    # Build Slack response for each question
    resp_qs.extend(map(get_response_string, so_qs[:max_questions]))

    return Response('\n'.join(resp_qs),
                    content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return redirect('https://github.com/karan/slack-overflow')


###########
# Helpers #
###########

def get_response_string(q):
    q_data = q.json
    check = ' :white_check_mark:' if q.json['is_answered'] else ''
    return "|%d|%s <%s|%s> (%d answers)" % (q_data['score'], check, q.url,
                                            q.title, q_data['answer_count'])
