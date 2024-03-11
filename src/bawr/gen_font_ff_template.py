# Copyright 2021 Frank David Martinez M.
# Copyright 2024 Lutz Schönemann
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

import fontforge, psMat
import os, sys, math

# +-------------------------------------------------------------------+
# | Start Generated Glyphs                                            |
# | defines: config, select, options, build_dir, global_transform,    |
# |          output_formats, verbose                                  |

#@generated

# | End Generated Glyphs                                              |
# +-------------------------------------------------------------------+

try:
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
except:
    sys.exit("Error creating directory: %s" % build_dir)   


def parse_transformation(t):
    '''
        ('t|translate', x, y)
        ('s|scale', x, y)
        ('r|rotate', deg)
        ('x|skew', deg)
    '''
    m = None
    if t:
        m = psMat.identity()
        for tx in t:
            if tx[0] == 't' or tx[0] == 'translate':
                m = psMat.compose(m, psMat.translate(tx[1], tx[2]))
            elif tx[0] == 'r' or tx[0] == 'rotate':
                m = psMat.compose(m, psMat.rotate(math.radians(tx[1])))
            elif tx[0] == 's' or tx[0] == 'scale':
                m = psMat.compose(m, psMat.scale(tx[1], tx[2]))
            elif tx[0] == 'x' or tx[0] == 'skew':
                m = psMat.compose(m, psMat.skew(math.radians(tx[1])))
    return m


font = fontforge.font()
font.encoding = "UnicodeFull"
font.copyright = config.font_copyright
font.familyname = config.font_family
font.fontname = config.font_name
font.fullname = config.font_name
font.version = config.font_version.strip() or font.version

for code, name, path, options in select:
    glyph = font.createChar(code, name)
    glyph.importOutlines(path)
    if options:
        lt = parse_transformation(options.get('font_transformation', None)) 
        if lt:
            glyph.transform(lt)
    if global_transform:
        glyph.transform(global_transform)

    if verbose:
        print("\n%s:\n  file: %s\n  code: %s" % (name, path, hex(code)))

for format in output_formats:
    font.generate('%s/%s.%s' % (build_dir, font.fontname, format))
