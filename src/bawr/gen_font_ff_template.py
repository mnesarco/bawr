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

# add latin characters to be used in
ligaChars = [
      (0x30, 'zero'),
      (0x31, 'one'),
      (0x32, 'two'),
      (0x33, 'three'),
      (0x34, 'four'),
      (0x35, 'five'),
      (0x36, 'six'),
      (0x37, 'seven'),
      (0x38, 'eight'),
      (0x39, 'nine'),

      (0x41, 'A'),
      (0x42, 'B'),
      (0x43, 'C'),
      (0x44, 'D'),
      (0x45, 'E'),
      (0x46, 'F'),
      (0x47, 'G'),
      (0x48, 'H'),
      (0x49, 'I'),
      (0x4a, 'J'),
      (0x4b, 'K'),
      (0x4c, 'L'),
      (0x4d, 'M'),
      (0x4e, 'N'),
      (0x4f, 'O'),
      (0x50, 'P'),
      (0x51, 'Q'),
      (0x52, 'R'),
      (0x53, 'S'),
      (0x54, 'T'),
      (0x55, 'U'),
      (0x56, 'V'),
      (0x57, 'W'),
      (0x58, 'X'),
      (0x59, 'Y'),
      (0x5a, 'Z'),

      (0x5f, 'underscore'),

      (0x61, 'a'),
      (0x62, 'b'),
      (0x63, 'c'),
      (0x64, 'd'),
      (0x65, 'e'),
      (0x66, 'f'),
      (0x67, 'g'),
      (0x68, 'h'),
      (0x69, 'i'),
      (0x6a, 'j'),
      (0x6b, 'k'),
      (0x6c, 'l'),
      (0x6d, 'm'),
      (0x6e, 'n'),
      (0x6f, 'o'),
      (0x70, 'p'),
      (0x71, 'q'),
      (0x72, 'r'),
      (0x73, 's'),
      (0x74, 't'),
      (0x75, 'u'),
      (0x76, 'v'),
      (0x77, 'w'),
      (0x78, 'x'),
      (0x79, 'y'),
      (0x7a, 'z'),
]

def mapCharToName(c):
    return {
        '0': 'zero',
        '1': 'one',
        '2': 'two',
        '3': 'three',
        '4': 'four',
        '5': 'five',
        '6': 'six',
        '7': 'seven',
        '8': 'eight',
        '9': 'nine',
        '_': 'underscore',
    }.get(c, c)

for code, name in ligaChars:
    glyph = font.createChar(code, name)
    pen = glyph.glyphPen()
    pen.moveTo(0,0)

lookup_name = '\'liga\' Standard Ligatures in Latin lookup 0'
subtable_name = lookup_name + ' subtable'
font.addLookup( lookup_name, "gsub_ligature", [], [ ("liga",[("latn",["dflt"])]) ] )
font.addLookupSubtable(lookup_name, subtable_name)

for code, name, path, options in select:
    glyph = font.createChar(code, name)
    glyph.importOutlines(path)

    ligature_components = ' '.join( map(mapCharToName, list(name)) )
    glyph.addPosSub(subtable_name, ligature_components)
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
