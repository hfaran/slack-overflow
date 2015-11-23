import flask
from flask import Flask, request, Response, redirect
from stackexchange import Sort, DESC

app = Flask(__name__)


@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow python list comprehension
    '''
    max_questions = flask._app_ctx_stack.max_questions
    so = flask._app_ctx_stack.so
    text = request.values.get('text')

    try:
        qs = so.search(intitle=text, sort=Sort.Votes, order=DESC)
    except UnicodeEncodeError:
        return Response(('Only English language is supported. '
                         '%s is not valid input.' % text),
                         content_type='text/plain; charset=utf-8')


    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    resp_qs.extend(map(get_response_string, qs[:max_questions]))

    if len(resp_qs) is 1:
        resp_qs.append(('No questions found. Please try a broader search or '
                        'search directly on '
                        '<https://stackoverflow.com|StackOverflow>.'))

    return Response('\n'.join(resp_qs),
                    content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return redirect('https://github.com/karan/slack-overflow')


def get_response_string(q):
    q_data = q.json
    check = ' :white_check_mark:' if q.json['is_answered'] else ''
    return "|%d|%s <%s|%s> (%d answers)" % (q_data['score'], check, q.url,
                                            q.title, q_data['answer_count'])
