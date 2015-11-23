import re

import html2text


class HTML2Slack(object):
    """Converts HTML from StackOverflow answers to Slack formatting"""
    def __init__(self):
        self.parser = self._configure_parser()
        self.md_link_regex = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def _configure_parser(self):
        """Create HTML2Text parser with optimal options for us"""
        h = html2text.HTML2Text()
        h.use_automatic_links = True
        # Marks code with [code]...[/code]; we have the parser mark this
        #  so that we can replace it later
        h.mark_code = True
        # Slack uses '*' rather than '**' for strong
        h.strong_mark = '*'
        return h

    @staticmethod
    def _convert_md_link_slack(match):
        """Returns replacement string in Slack format from Markdown match"""
        label, link = match.groups()
        # In case there were any newlines inserted, we get rid of them
        #  so that the links aren't broken up and Slack can parse them
        label = label.replace('\n', '')
        link = link.replace('\n', '')
        # Return in Slack's native <url|label> format
        return "<{}|{}>".format(link, label)

    def handle(self, html):
        """Convert html into Slack formatted string

        :type html: str
        :rtype: str
        """
        s = self.parser.handle(html)
        # Replace instances of marked code
        s = s.replace("[code]", "```")
        s = s.replace("[/code]", "```")
        # Make markdown links into slack links
        s = re.sub(self.md_link_regex, self._convert_md_link_slack, s)
        return s

h = HTML2Slack()


def html2slack(html):
    s = h.handle(html)
    return s
