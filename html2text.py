# Copyright 2016 Mayo Yamasaki. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0.
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# ==============================================================================
import argparse
from html.parser import HTMLParser
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


class Parser(HTMLParser):
    BLOCKS = ['p', 'div', 'table', 'dl', 'ul',
              'ol', 'form', 'address', 'blockquote', 'h1',
              'h2', 'h3', 'h4', 'h5', 'h6', 'fieldset',
              'hr', 'pre''article', 'aside', 'dialog',
              'figure', 'footer', 'header', 'legend', 'nav',
              'section']
    IGNORES = ['style', 'script', 's']

    def __init__(self):
        self.reset()
        self.convert_charrefs= True
        self.fed = []
        self.current_tag = 'INIT_VALUE'

    def handle_startendtag(self, tag, _):
        self.current_tag = tag.lower()

    def handle_data(self, data):
        if self.current_tag in self.IGNORES: return
        self.fed.append(data)

    def handle_endtag(self, tag):
        # to bypass extract from '<p>foo</p>bar' to 'foobar'
        # this case potentially failed to be tokenized
        if tag in self.BLOCKS:
            self.fed.append('\n')

    def get_data(self):
        text = ''.join(self.fed)

        # normailze space letter
        text = text.replace('\t', ' ').replace('\xa0', ' ')

        # compress space letters
        text = re.sub(r' +', ' ', text)

        # delete space and filter blank sentences.
        text = '\n'.join(
            filter(lambda x: x != '',
                map(lambda s: s.strip(), text.split('\n'))
            )
        )

        return text


def html2text(html):
    """ extract full text from HTML tagged text """
    p = Parser()
    p.feed(html)
    return p.get_data()


def main():
    parser = argparse.ArgumentParser(
            description="extract text from HTML for text processing.")

    parser.add_argument('input',
                        help="input file or url.")

    parser.add_argument('-b', '--body-not-extract',
                        action='store_false',
                        help="**not** extract main body text from html using buriy's readability")

    args = parser.parse_args()

    if args.input.startswith('http://') or args.input.startswith('https://'):
        html = url2html(args.input)
    else:
        html = sys.stdin

    if args.body_not_extract:
        html  = html2body(html)

    text = html2text(html)
    print(text)


if __name__ == '__main__':
    main()
