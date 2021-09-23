# Copyright 2021 Frank David Martinez Muñoz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in 
# the Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION 
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re

RE_GLYPH_NAME = re.compile(r'^[a-zA-Z](\w)*$')
RE_GLYPH_BADCHAR = re.compile(r'\W+')

def get_glyph_name(name):
    glyph_name = RE_GLYPH_BADCHAR.sub("_", name)
    if not RE_GLYPH_NAME.match(glyph_name):
        print("[error] Invalid glyph name {} from {}".format(glyph_name, name))
    return glyph_name

class Glyph:
    def __init__(self, code, name, path, source):
        self.code = code
        self.name = get_glyph_name(name)
        self.path = path
        self.source = source

    def __repr__(self):
        return "{}:{}:{:x} ({})".format(self.source.__name__, self.name, self.code, self.path)

