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

class CppAtlasHeader:
    name = None
    namespace = None
    constexpr = True
    source = None
    instance = None
    output = None

    def build(self, env):
        print(f"[Cpp Atlas Header] Start ...")
        if not self.source or not self.source.instance:
            print(f"[Cpp Atlas Header] Invalid source (CppAtlasHeader.source)")
            return
        
        atlas = self.source.instance
        hpp_file = Path(env.BAWR_OUTPUT_DIR, (self.name or atlas.name or 'icons') + '_cells.hpp')
        print(f"[Cpp Atlas Header] {hpp_file}")

        constexpr = 'constexpr' if self.constexpr else 'const'

        with open(hpp_file, 'w') as f:
            f.write("#pragma once\n\n")
            f.write("struct ImVec2;\n")
            f.write(f"namespace {self.namespace or 'icons'} {{\n")
            f.write( " struct uv { float x; float y; inline operator ImVec2 const& () const { return *reinterpret_cast<const ImVec2*>(this); } };\n")
            f.write( " struct frame { uv uv0; uv uv1; };\n")

            icons = atlas.cells
            width = atlas.width
            height = atlas.height
            for size in atlas.sizes:
                f.write(f" struct sz{size} {{\n")
                for icon in icons:
                    u0 = icon.x / width
                    v0 = icon.y / height
                    u1 = u0 + (icon.width / width)
                    v1 = v0 + (icon.height / height)
                    if icon.width == size:
                        f.write(f"   static {constexpr} frame {icon.name.ljust(24)} {{{{{u0:.10f},{v0:.10f}}},{{{u1:.10f},{v1:.10f}}}}};\n")
                f.write(f" }};\n")
            f.write( "}\n")

        self.output = hpp_file