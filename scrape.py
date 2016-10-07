#
# Extract body and title text from Website URL
#

import re
import urllib.request
from readability.readability import Document
from html2text import html2text


def extract_content(url):
    """ get text and title from website URL"""

    headers = {
        "User-Agent" :  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    }

    req = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(req) as response:
        html = response.read()

    if html is None:
        raise("[Error] Can't get HTML. {}".fomat(url))

    d = Document(html)
    title, body_html = d.short_title(), d.summary()

    #body = re.sub(r" +", " ", html2text(sanitize(body_html)))
    body = html2text(body_html)
    ## delete space and filter blank sentences.
    #body = '\n'.join(
    #    filter(lambda x: x != '',
    #        map(lambda s: s.strip(), body.split('\n'))
    #    )
    #)
    return (title, body)


def sanitize(text):
    """ Sanitize test """
    # delete tab and unicorde space.
    text = text.replace('\t', ' ').replace('\xa0', ' ')
    # eliminate concat error such as "foo</X><Y>bar -> foobar"
    text = re.sub(r"><", "> <", text)
    return text


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

    s = MLStripper()
    s.feed(html)
    return s.get_data()


def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(
            description="Scrape title and body text from URL.")

    parser.add_argument('url',
                        action='store',
                        type=str,
                        help='target url as string')
    parser.add_argument('-d', '--destinaiton',
                        action='store',
                        nargs='?',
                        default=sys.stdout,
                        type=argparse.FileType('w'),
                        help='title + body text output file path')
    args = parser.parse_args()

    title, body = extract_content(args.url.rstrip('\n'))
    args.destinaiton.write(title + '\n' + body)


if __name__ == '__main__':
    main()
