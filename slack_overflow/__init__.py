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
    Displays Slack-formatted most-upvoted answer of the most upvoted
    question from the query.

    soi ~ StackOverflow-Inline

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
    if not so_qnids:
        return "*No questions for the given query were found! :(*"
    # Fetch Questions using SO API
    so_qs = so.questions(so_qnids)
    # Sort Questions by score
    so_qs = sorted(so_qs, key=lambda q: q.score, reverse=True)

    top_question = so_qs[0]
    answer_body = get_question_top_answer_body(so=so, question=top_question)
    question_str = get_response_string(top_question)

    resp_list = [question_str]
    if answer_body is None:
        resp_list.append("\n\n*The top question for your query is unanswered! "
                         ":(*")
    else:
        resp_list.append("\n\n")
        resp_list.append(html2slack(answer_body))

    return Response("".join(resp_list),
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
    if not so_qnids:
        return "*No questions for the given query were found! :(*"
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
    return redirect('https://github.com/hfaran/slack-overflow')


###########
# Helpers #
###########

def get_response_string(q):
    q_data = q.json
    check = ' :white_check_mark:' if q.json['is_answered'] else ''
    return "|%d|%s <%s|%s> (%d answers)" % (q_data['score'], check, q.url,
                                            q.title, q_data['answer_count'])
