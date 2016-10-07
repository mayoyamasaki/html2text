# Copyright 2016 Mayo Yamasaki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0.
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================
import argparse
import re
from readability.readability import Document
import sys
import urllib.request


def url2html(url):
    """get html from internet url"""
    headers = {
        "User-Agent" :  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

    req = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(req) as response:
        html = response.read()

    if html is None:
        raise Exception("Failed to get HTML from" +  str(url))
    return html


def html2body(html):
    """ extract title and body from html"""
    d = Document(html)
    title, body = d.short_title(), d.summary()
    return title + '\n' + body


def html2text(html):
    """ extract full text from HTML tagged text """
    from html.parser import HTMLParser
    class MLStripper(HTMLParser):
        def __init__(self):
            self.reset()
            self.strict = False
            self.convert_charrefs= True
            self.fed = []
        def handle_data(self, d):
            self.fed.append(d)
        def get_data(self):
            return ''.join(self.fed)

    def sanitize(text):
        """ Sanitize test """
        # delete tab and unicorde space.
        text = text.replace('\t', ' ').replace('\xa0', ' ')
        # eliminate concat error such as "foo</X><Y>bar -> foobar"
        text = re.sub(r"><", "> <", text)
        return text

    s = MLStripper()
    s.feed(sanitize(html))
    text = re.sub(r" +", " ", s.get_data())
    # delete space and filter blank sentences.
    text = '\n'.join(
        filter(lambda x: x != '',
            map(lambda s: s.strip(), text.split('\n'))
        )
    )
    return text


def main():
    parser = argparse.ArgumentParser(
            description="extract text from HTML for text processing.")

    parser.add_argument('input',
                        help="input file or url.")

    parser.add_argument('-b', '--body-extract',
                        action='store_false',
                        help="**not** extract main body text from html using buriy's readability")

    args = parser.parse_args()

    if args.input.startswith('http://') or args.input.startswith('https://'):
        html = url2html(args.input)
    else:
        html = sys.stdin

    if args.body_extract:
        html  = html2body(html)

    text = html2text(html)
    print(text)


if __name__ == '__main__':
    main()
