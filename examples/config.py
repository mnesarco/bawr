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

#------------------------------------------------------------------------------
# Import all required stuff:
#------------------------------------------------------------------------------

from bawr.config import *

#------------------------------------------------------------------------------
# Define an environment (Use the name that you want, but extend Environment):
#------------------------------------------------------------------------------

class Env( Environment ):

    # [Optional] FONTFORGE_PATH = Path to fontforge executable, deduced if it is in PATH
    # FONTFORGE_PATH = ...

    # [Optional] INKSCAPE_PATH = Path to inkscape executable, deduced if it is in PATH
    # INKSCAPE_PATH = ...   

    # [Optional] BAWR_OUTPUT_DIR = Where all the output will be generated. Default = ./build
    # BAWR_OUTPUT_DIR = ...

    # [Optional] BAWR_SOURCE_DIR = Where all the icon folders will be found. Default = ./
    #  BAWR_SOURCE_DIR = ...

    pass

#------------------------------------------------------------------------------
# Define your icon sets (extend IconSet):
#------------------------------------------------------------------------------

class BootstrapIcons( IconSet ):

    # [Mandatory] src = directory name (which contains svg icons)
    src = 'bootstrap-icons'

    # [Optional] select = selection of icons from the directory: list( tuple(file-name, glyph-name) )
    select = [
        ('info-circle',              'infoCircle'),
        ('file-earmark',             'fileEarmark'),
        ('folder2-open',             'folderOpen'),
        ('hdd',                      'save'),
        ('file-earmark-arrow-up',    'fileImport'),
        ('file-earmark-arrow-down',  'fileExport'),
        ('folder',                   'folder'),
        ('sliders',                  'sliders'),
        ('eye',                      'eye'),
        ('layers',                   'layers'),
    ]

    # [Optional] options = Special options for generators
    options = {
        "font_transformation": [('scale', 0.75, 0.75)],
        "atlas_preprocessors": [
            RegexReplacePreprocessor(
                {
                    "currentColor": "#ffffff",
                    'width="1em"': 'width="16"',
                    'height="1em"': 'height="16"',
                }            
            )
        ],
        "atlas_margin": 0.0625
    }

# Another icon set with different options

class MyIcons( IconSet ):

    src = 'icons'

    options = {
        "atlas_preprocessors": [
            RegexReplacePreprocessor(
                {
                    'fill:#000000': "fill:#ffffff",
                    'stroke:#000000': 'stroke:#ffffff',
                }            
            )
        ]
    }

#------------------------------------------------------------------------------
# [Optional]
# Define Font generator to generate truetype fonts using FontForge
# (extend Font)
#------------------------------------------------------------------------------

class MyFont( Font ):

    # Generated font copyright notice [Mandatory]
    copyright = "Copyright 2020 Frank D. Martinez M."

    # Font name [Mandatory]
    name = "my-icons"

    # Font family [Mandatory]
    family = "my-icons"

    # First font glyph code [Optional] (default = 0xe000)
    # start_code = 0xe000

    # List or tuple of the icon sets included in this font [Mandatory]
    collections = (BootstrapIcons, MyIcons)

    # Global font transformation [Optiona] (See: Font transformations)
    # transformation = []

    # Output format [Optional] (default = ['ttf'])
    # output_formats = ['ttf']

    # Verbose output. Shows glyph generation details [Optional] (default = False)
    # verbose = False


#------------------------------------------------------------------------------
# [Optional]
# You can generate a C++ font header file with glyph codes ready to use in C++.
# (extend CppFontHeader)
#------------------------------------------------------------------------------

class MyCppFontH( CppFontHeader ):

    # [Mandatory] Reference to the font generator to use
    source = MyFont    

    # [Optional] Generate constexpr values (default = false)
    constexpr = True

    # [Optional] name of the generated c++ file (default = source.name)
    # name = ...

    # [Optional] namespace of the generated c++ file (default = icons)
    # namespace = ...

    # [Optional] Generate macros (default = True)
    # macros = ...

    # [Optional] Prefix for all macros (default = Icon_)
    # macro_prefix = ...


#------------------------------------------------------------------------------
# [Optional]
# You can Embed your font binary into a C++ source file to be linked.
# (extend CppEmbedded)
#------------------------------------------------------------------------------

class MyCppFontEmbed( CppEmbedded ):

    # [Mandatory] Reference to the binary file to embed
    source = "${BAWR_OUTPUT_DIR}/my-icons.ttf"

    # [Optional] name prefix for the generated files (default = source name)
    # name = ...

    # [Optional] namespace for the generated files (default = icons)
    # namespace = ...


#------------------------------------------------------------------------------
# [Optional]
# You can generate C++ code to load your font into Dear ImGui.
# (extend CppEmbedded)
#------------------------------------------------------------------------------

class MyCppFontImGui( ImGuiFontLoader ):

    # [Mandatory] reference to the font
    font = MyFont

    # [Mandatory] reference to the font header
    header = MyCppFontH    

    # [Mandatory] reference to the embedded binary
    data = MyCppFontEmbed

    # [Optional] name prefix for the generated files (default = font.name)
    # name = ...

    # [Optional] namespace for the generated files (default = icons)
    # namespace = ...

#------------------------------------------------------------------------------
# [Optional]
# You can generate an optimized png atlas with all your icons in different sizes.
# (extend Atlas)
#------------------------------------------------------------------------------

class MyAtlas( Atlas ):

    # [Optional] width of the atlas image (default = 512)
    width = 512

    # [Mandatory] sizes of the icons to be generated and included in the atlas
    sizes = (16, 32, 64)

    # [Mandatory] References to collections (icon sets) to be included
    collections = (BootstrapIcons, MyIcons)

    # [Optional] name prefix for the generated files (default = font.name)
    # name = ...

# [Optional] Embed the Atlas png into a C++ source.
class MyCppAtlasEmbed( CppEmbedded ):
    source = "${BAWR_OUTPUT_DIR}/atlas.png"

#------------------------------------------------------------------------------
# [Optional]
# Generate a C++ header file with the atlas cells (frames) to be used in your code.
# (extend CppAtlasHeader)
#------------------------------------------------------------------------------

class MyAtlasHeader( CppAtlasHeader ):
    source = MyAtlas

