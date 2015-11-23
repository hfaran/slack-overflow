# -*- coding: utf-8 -*- 

import os

import click
from flask import Flask, request, Response, redirect
from stackexchange import Site, StackOverflow, Sort, DESC

try:
    import config
    se_key = config.stackexchange['api_key']
except:
    se_key = os.environ.get('SE_KEY')


if not se_key:
    import sys
    print 'No config.py file found. Exiting...'
    sys.exit(0)


MAX_QUESTIONS = 5


app = Flask(__name__)
so = Site(
    StackOverflow,
    se_key
)


def get_response_string(q):
    q_data = q.json
    check = ' :white_check_mark:' if q.json['is_answered'] else ''
    return "|%d|%s <%s|%s> (%d answers)" % (q_data['score'], check, q.url,
                                            q.title, q_data['answer_count'])


@app.route('/overflow', methods=['post'])
def overflow():
    '''
    Example:
        /overflow python list comprehension
    '''
    text = request.values.get('text')

    try:
        qs = so.search(intitle=text, sort=Sort.Votes, order=DESC)
    except UnicodeEncodeError:
        return Response(('Only English language is supported. '
                         '%s is not valid input.' % text),
                         content_type='text/plain; charset=utf-8')


    resp_qs = ['Stack Overflow Top Questions for "%s"\n' % text]
    resp_qs.extend(map(get_response_string, qs[:MAX_QUESTIONS]))

    if len(resp_qs) is 1:
        resp_qs.append(('No questions found. Please try a broader search or '
                        'search directly on '
                        '<https://stackoverflow.com|StackOverflow>.'))

    return Response('\n'.join(resp_qs),
                    content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return redirect('https://github.com/karan/slack-overflow')


def envvar(name, default):
    """Create callable environment variable getter

    :param str name: Name of environment variable
    :param default: Default value to return in case it isn't defined
    """
    return lambda: os.environ.get(name, default)


@click.command()
@click.option('-p', '--port', default=envvar('PORT', '5000'),
              type=click.INT)
def main(port):
    app.run(
        host='0.0.0.0',
        port=port
    )


if __name__ == '__main__':
    main()
