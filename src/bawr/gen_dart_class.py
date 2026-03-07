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

class DartClass:

    # Config
    name = None
    source = None

    # Generated
    instance = None
    output = None

    def build(self, env):
        print("[Dart Class] Start ...")

        if self.source is None or self.source.instance is None:
            print("[Dart Class] Invalid source (DartClass.source)")
            return

        instance = self.source.instance
        icons = instance.icons
        build_dir = env.BAWR_OUTPUT_DIR

        name = (self.name or instance.name or "icons").replace("-", "_")
        dart_file = Path(build_dir, name + ".dart")
        self.output = dart_file
        print(f"[Dart Class] {str(dart_file)}")
        with open(dart_file, 'w') as f:
            f.write(f'// Generated with bawr: {datetime.now()}\n\n')
            f.write("import 'package:flutter/widgets.dart';\n\n")
            f.write(f'class {self.__class__.__name__}\n{{\n')
            f.write(f'    static const {"Font_Family":<32} = "{instance.family}";\n')
            f.write(f'    static const {"Font_StartCode":<32} = {hex(instance.start_code)};\n')
            f.write(f'    static const {"Font_EndCode":<32} = {hex(instance.end_code)};\n')
            for glyph in icons:
                if glyph.code > 0:
                    code = hex(glyph.code)
                    f.write(f'    static const IconData {glyph.name:<32} = IconData({code}, fontFamily: Font_Family);\n')
            f.write('}\n')

