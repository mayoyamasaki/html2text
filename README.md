# html2text
html2text is a shiple python3.x implementation text extractor that convert html to tokenizable utf-8 text which can be easily tokenized.

## Requirements
- you should install [readability](https://github.com/buriy/python-readability) module.

## Useage
```
usage: html2text.py [-h] [-b] input

extract text from HTML for text processing.

positional arguments:
  input               input file or url.

optional arguments:
  -h, --help          show this help message and exit
  -b, --body-extract  **not** extract main body text from html using buriy's
                      readability
```

For example, you can use it.

```
python3 html2text.py https://example.com > example.com.txt
```

Or you can use it with Python.

```
$ python3
>>> import html2text
>>> html = html2text.url2html('https://example.com')
>>> bodyhtml = html2text.html2body()
>>> text = html2text.html2text()
```

## License
This code is under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) license.
