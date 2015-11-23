import re
from urlparse import urlparse

import flask
from flask import Flask, request, Response, redirect
from stackexchange import Sort, DESC

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
    max_questions = flask._app_ctx_stack.max_questions
    so = flask._app_ctx_stack.so
    text = request.values.get('text')

    # try:
    #     qs = so.search(intitle=text, sort=Sort.Votes, order=DESC)
    # except UnicodeEncodeError:
    #     return Response(('Only English language is supported. '
    #                      '%s is not valid input.' % text),
    #                      content_type='text/plain; charset=utf-8')
    #
    #
    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    # resp_qs.extend(map(get_response_string, qs[:max_questions]))
    #
    # if len(resp_qs) is 1:
    #     resp_qs.append(('No questions found. Please try a broader search or '
    #                     'search directly on '
    #                     '<https://stackoverflow.com|StackOverflow>.'))
    question_regex = re.compile('^/questions/(\d+)/')
    def get_question_nid(match):
        if match is None:
            return None
        return int(match.groups()[0])

    so_qs = []
    pages = max_questions//10 + 1
    sr = search("site:stackoverflow.com/questions {}".format(text), pages=pages)
    for result in sr:
        purl = urlparse(result.link)
        print purl
        assert purl.netloc == 'stackoverflow.com', "Non-StackOverflow result; search is broken!"
        qnid = get_question_nid(question_regex.match(purl.path))
        if qnid is not None:
            so_qs.append(so.question(qnid))
    so_qs = sorted(so_qs, key=lambda q: q.score, reverse=True)
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
