import sys; sys.path.append(".")

from mock import Mock

from slack_overflow.html2slack import html2slack
from slack_overflow.html2slack import HTML2Slack


def test___convert_md_link_slack():
    match = Mock()
    match.groups.return_value = label, link = \
        "Exa\nmple", "http://exa\nmple.com"
    assert HTML2Slack._convert_md_link_slack(match) == \
           "<http://example.com|Example>"


def test__html2slack():
    html = """
    <pre><code>foobar</code></pre>
    """
    slack = html2slack(html)
    assert slack.strip() == "```\n\n    foobar\n```"
