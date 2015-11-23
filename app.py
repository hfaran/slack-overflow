# -*- coding: utf-8 -*- 

import os

import click
import flask
from stackexchange import Site, StackOverflow

from slack_overflow import app
from slack_overflow.util import envvar


@click.command()
@click.option('-p', '--port', default=envvar('PORT', '5000'),
              type=click.INT)
@click.option('-m', '--max-questions', default=envvar('MAX_QUESTIONS', '5'),
              type=click.INT)
@click.option('--se-key', default=envvar('SE_KEY', ''),
              type=click.STRING)
@click.option('--debug', is_flag=True,
              default=lambda: os.environ.get('FLASK_DEBUG') == '1')
def main(port, max_questions, se_key, debug):
    so = Site(
        domain=StackOverflow,
        app_key=se_key if se_key else None
    )

    app.debug = debug
    if app.debug:
        print("WARNING: DEBUG MODE IS ENABLED!")
    app.config["PROPAGATE_EXCEPTIONS"] = True

    top = flask._app_ctx_stack
    top.so = so
    top.max_questions = max_questions

    app.run(
        host='0.0.0.0',
        port=port
    )


if __name__ == '__main__':
    main()
