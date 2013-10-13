json2html-bookmarks
===================

Convert Firefox bookmarks from JSON to HTML format (can be imported in other browsers)

Tested with Python 2.4 - 3.3. For Python < 2.6, the module simplejson (https://pypi.python.org/pypi/simplejson/) is required.

Usage
-----

python json2html.py json_bookmark_input [html_bookmark_output]

Convert json_bookmark_input from the JSON bookmarks format to the HTML format.
The output is written on the standard output or optionally on a file.

