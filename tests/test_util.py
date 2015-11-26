import sys; sys.path.append(".")

import os

from slack_overflow.util import envvar


def test__envvar():
    ENVVAR = "_SLACK_OVERFLOW_TESTVAR"
    f = envvar(ENVVAR, "default")
    assert f() == "default"
    os.environ[ENVVAR] = "foobar"
    assert f() == "foobar"
    del os.environ[ENVVAR]
    assert f() == "default"
