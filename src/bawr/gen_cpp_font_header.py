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

from pathlib import Path
from datetime import datetime

class CppFontHeader:

    # Config
    name = None
    namespace = None
    constexpr = False
    macros = True
    macro_prefix = 'Icon_'
    source = None

    # Generated
    instance = None
    output = None

    def build(self, env):
        print("[CPP Font Header] Start ...")

        if self.source is None or self.source.instance is None:
            print(f"[CPP Font Header] Invalid source (CppFontHeader.source)")
            return

        instance = self.source.instance
        icons = instance.icons
        build_dir = env.BAWR_OUTPUT_DIR
        self.namespace = self.namespace or 'icons'
        namespace = self.namespace

        header_file = Path(build_dir, self.name or instance.name + "_codes.hpp")
        self.output = header_file
        print(f"[CPP Font Header] {str(header_file)}")
        with open(header_file, 'w') as f:
            f.write(f'#pragma once\n\n')
            f.write(f'// Generated: {datetime.now()}\n\n')

            if self.macros:
                f.write(f'#define {self.macro_prefix}{"Font_Family":<32} "{instance.family}"\n')
                f.write(f'#define {self.macro_prefix}{"Font_StartCode":<32} {hex(instance.start_code)}\n')
                f.write(f'#define {self.macro_prefix}{"Font_EndCode":<32} {hex(instance.end_code)}\n')
                for glyph in icons:
                    if glyph.code > 0:
                        code = "U+" + hex(glyph.code)[2:]
                        literal = repr( chr(glyph.code).encode( 'utf-8' ))[ 2:-1 ]
                        f.write(f'#define {self.macro_prefix}{glyph.name:<32} "{literal}" //< {code}\n')

            if self.constexpr:
                constexpr = 'constexpr'
            else:
                constexpr = 'const'

            f.write(f'\nnamespace {namespace}\n{{\n')       
            f.write(f'    {constexpr} auto {"Font_Family":<32} = "{instance.family}";\n')
            f.write(f'    {constexpr} auto {"Font_StartCode":<32} = {hex(instance.start_code)};\n')
            f.write(f'    {constexpr} auto {"Font_EndCode":<32} = {hex(instance.end_code)};\n')
            for glyph in icons:
                if glyph.code > 0:
                    code = "U+" + hex(glyph.code)[2:]
                    literal = repr( chr(glyph.code).encode( 'utf-8' ))[ 2:-1 ]
                    f.write(f'    {constexpr} auto {glyph.name:<32} = "{literal}"; //< {code}\n')

            f.write(f'\n    namespace code\n    {{\n')       
            for glyph in icons:
                if glyph.code > 0:
                    code = "U+" + hex(glyph.code)[2:]
                    literal = repr( chr(glyph.code).encode( 'utf-8' ))[ 2:-1 ]
                    f.write(f'        {constexpr} auto {glyph.name:<32} = "{code}"; //< {literal}\n')
            f.write('    }\n')

            f.write('}\n')

