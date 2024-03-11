# BAWR

This is a tool to automate the icons generation from sets of svg files into fonts and atlases.

The main purpose of this tool is to add it to the build process of your c++ project and let it do all the work, then you can use your svg icons as fonts
or as spritesheets.

The project url is: https://github.com/mnesarco/bawr
This project is based on a previous project: https://github.com/mnesarco/ff-batch 

## Features

- Generate TrueType fonts from svg collections.
- Generate png textures from svg collections.
- Embed binaries into c++ sources ready to link.
- Generate ImGui Font Loaders (c++). ([howto](https://github.com/mnesarco/bawr/blob/main/ImGui.md))
- Generate c++ Atlas Maps.
- Generate c++ Font constants as Macros and/or as const/constexpr.
- Apply transformation to svg files during the generation.
  - Textual transformations
  - Font forge supported transformations

## Requirements

- Python 3.6+
- FontForge 20170924+
- Inkscape 1.0+

## Install

Build from sources

```bash
git clone https:://github.com/mnesarco/bawr.git
cd bawr

python3 -m pip install --upgrade build
python3 -m pip install wheel

python3 -m build 
python3 -m pip install dist/bawr-0.0.6-py3-none-any.whl

```

Or from pypi:

```bash
python3 -m pip install bawr
```


## Terminology

| Concept                | Description                                                                                           |
|------------------------|-------------------------------------------------------------------------------------------------------|
| Svg Icon               | It is just a file in .svg format. It must be a square.                                                |
| Icon set or Collection | It is a folder with svg icons                                                                         |
| Configuration file     | It is a python file with all the options to generate your files. By convention it is called config.py |

## Usage

1. Create a folder
2. Put a file named `config.py` (you can copy the one from examples dir https://github.com/mnesarco/bawr/tree/main/examples)
3. Add folders with svg icons
4. Adjust the configuration (edit config.py)
5. Call bawr

```bash
cd examples
python3 -m bawr.tool

```

## Examples

You can use the examples dir (https://github.com/mnesarco/bawr/tree/main/examples) as a template for your project:

```bash
examples/
├── config.py
├── icons/
└── bootstrap-icons/

```

### Result (generated files):

```bash
examples/build/
├── atlas_cells.hpp
├── atlas.cpp
├── atlas.hpp
├── atlas.png
├── my-icons_codes.hpp
├── my-icons.cpp
├── my-icons.hpp
├── my-icons_loader.hpp
└── my-icons.ttf

```

## Configuration (`config.py`)

```python
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

    # List ot tuple of the icon sets included in this font [Mandatory]
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


```

## How to use with Dear ImGui:

https://github.com/mnesarco/bawr/blob/main/ImGui.md

## What is in the name

**BAWR** in honor of **Bertrand Arthur William Russell**, a great Logician, Mathematician and Philosopher of the IX and XX centuries. 