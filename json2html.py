#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Convert Firefox bookmarks from JSON to HTML format
#
# Copyright (c) 2013 Andrea Bonomi - andrea.bonomi@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# v 1.0 - 2013/10/12
#

import sys
import math
import codecs

try:
    import json
except:
    # Python < 2.6
    try:
        import simplejson as json
    except:
        sys.stderr.write("%s: Please install the required module 'simplejson'.\n" % sys.argv[0])
        sys.exit(1)

if sys.version > '3':
    long = int

def err():
    e = sys.exc_info()[1]
    sys.stderr.write(u"%s: %s\n" % (sys.argv[0], str(e)))
    sys.exit(1)

def printi(output, indent, string):
    if sys.version > '3':
        output.buffer.write((u" " * 4 * indent + string + "\n").encode('utf-8'))
    else:
        output.write((" " * 4 * indent) + string.encode('utf-8') + "\n")

def convert_time(time):
    try:
        return long(math.floor(long(time) / 1000000))
    except:
        return ""

def p(output, data, indent=0):
    children = data.get('children', None)
    uri = data.get('uri', None)
    if isinstance(children, list):
        if indent == 0:
            # Output the main header
            printi(output, indent, u"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
    It will be read and overwritten.
    DO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>%s</H1>
<DL><p>""" % (data.get('title', 'Bookmarks Menu')))
        else:
            # Output a folder
            date_added = 'dateAdded' in data and ' ADD_DATE="%s"' % convert_time(data.get('dateAdded')) or ''
            last_modified = 'lastModified' in data and ' LAST_MODIFIED="%s"' % convert_time(data.get('lastModified')) or ''
            title = data.get('title', '')
            printi(output, indent, '<DT><H3%s%s>%s</H3>' % (date_added, last_modified, title))
            printi(output, indent, '<DL><p>')
        # Output the children of a folder/main
        for child in children:
            p(output, child, indent+1)
        printi(output, indent,'</DL><p>')
    if uri is not None:
        # Output a bookmark
        date_added = 'dateAdded' in data and ' ADD_DATE="%s"' % convert_time(data.get('dateAdded')) or ''
        last_modified = 'lastModified' in data and ' LAST_MODIFIED="%s"' % convert_time(data.get('lastModified')) or ''
        title = data.get('title', uri)
        printi(output, indent, '<DT><A HREF="%s"%s%s>%s</A>' % (uri, date_added, last_modified, title))
        annos = data.get('annos', None)
        if isinstance(annos, list):
            for anno in annos:
                if isinstance(anno, dict) and anno.get('name') == 'bookmarkProperties/description':
                    printi(output, indent, '<DD>%s' % anno.get('value'))

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        sys.stderr.write(u"Convert bookmarks stored in JSON to HTML\n")
        sys.stderr.write(u"usage: %s json_bookmark_input [html_bookmark_output]\n" % sys.argv[0])
        sys.exit(2)
    filename = sys.argv[1]
    output_filename = len(sys.argv) > 2 and sys.argv[2] or None
    try:
        f = codecs.open(filename, "r", "utf-8")
        data = json.loads(f.read())
        f.close()
        if output_filename:
            output = open(output_filename, "w")
        else:
            output = sys.stdout
        p(output, data.get('children')[0])
        if output_filename:
            output.close()
    except (Exception):
        err()
    sys.exit(0)

if __name__ == '__main__':
    main()

