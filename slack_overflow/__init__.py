import logging

import flask
from flask import Flask, request, Response, redirect

from slack_overflow.stackoverflow import extract_question_nid_from_url
from slack_overflow.stackoverflow import google_search_stackoverflow_query
from slack_overflow.stackoverflow import get_question_top_answer_body
from slack_overflow.html2slack import html2slack


app = Flask(__name__)


############
# Handlers #
############

@app.route('/soi', methods=['post'])
def soi():
    '''
    Example:
        /soi python list comprehension
    '''
    # Get objects on the application context pushed on startup
    so = flask._app_ctx_stack.so

    text = request.values.get('text')

    # Perform google search
    sr = google_search_stackoverflow_query(text, pages=1)
    # Extract each question nid from results
    so_qnids = []
    for result in sr:
        qnid = extract_question_nid_from_url(result.link)
        if qnid is not None:
            so_qnids.append(qnid)
        else:
            logging.warning("Found invalid URL in search: "
                            "{}".format(result.link))
    # Fetch Questions using SO API
    so_qs = so.questions(so_qnids)
    # Sort Questions by score
    so_qs = sorted(so_qs, key=lambda q: q.score, reverse=True)

    answer_body = get_question_top_answer_body(so=so, question=so_qs[0])
    if answer_body is None:
        return "The top question for your query is unanswered!"
    # # Build Slack response for each question
    # resp_qs.extend(map(get_response_string, so_qs[:max_questions]))

    # return Response('\n'.join(resp_qs),
    #                 content_type='text/plain; charset=utf-8')
    print(unicode(answer_body))
    print(html2slack(answer_body))
    return Response("\n\n\n".join([answer_body, html2slack(answer_body)]),
                    content_type='text/plain; charset=utf-8')


@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow python list comprehension
    '''
    # Get objects on the application context pushed on startup
    max_questions = flask._app_ctx_stack.max_questions
    so = flask._app_ctx_stack.so
    # Each page in the google search has ten entries
    pages = max_questions//10 + 1

    text = request.values.get('text')

    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    # Perform google search
    sr = google_search_stackoverflow_query(text, pages=pages)
    # Extract each question nid from results
    so_qnids = []
    for result in sr:
        qnid = extract_question_nid_from_url(result.link)
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
