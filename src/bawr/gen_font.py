# Copyright 2021 Frank David Martinez Muñoz
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

from pathlib import Path
import os
from bawr.glyph import Glyph
from bawr import utils
from bawr.tool_fontforge import FontForgeTool

class Font:

    # Config
    copyright = "Copyright 2021 Frank David Martinez M."
    name = "icons"
    family = "icons"
    version = ''
    start_code = 0xe000
    collections = []
    transformation = []
    output_formats = ('ttf',)
    verbose = False

    # Generated
    icons = []
    instance = None

    def build(self, env):
        print("[Font Forge] Start ...")
        code = self.start_code
        for icon_set_cls in utils.as_iterable(self.collections):
            icon_set = icon_set_cls()
            if icon_set.select:
                for file_name, glyph_name in icon_set.select:
                    self.icons.append(Glyph(code, glyph_name, Path(env.BAWR_SOURCE_DIR, icon_set.src, file_name + ".svg"), icon_set_cls))
                    code += 1
            else:
                source = Path(env.BAWR_SOURCE_DIR, icon_set.src)
                if source.exists():
                    for file in sorted(os.listdir(source)):
                        if file[-4:].lower() != '.svg':
                            continue
                        stem = file[:-4].lower()
                        self.icons.append(Glyph(code, stem, Path(env.BAWR_SOURCE_DIR, icon_set.src, file), icon_set_cls))
                        code += 1
                else:
                    print("[error] Invalid source dir: {}".format(source.absolute()))
        self.end_code = code - 1 if code != self.start_code else None
        self.generate(env)
        self.run(env)

        print("")
        for fmt in self.output_formats:
            print("[Font Forge] {}".format(Path(env.BAWR_OUTPUT_DIR, "{}.{}".format(self.name, fmt))))


    def generate(self, env):
        cache_dir = utils.get_cache_dir(env) 
        with open(Path(Path(__file__).parent, 'gen_font_ff_template.py')) as f:
            pre, discard, pos = f.read().partition("#@generated")
            with open(Path(cache_dir, '_ff_.py'), 'w') as out:
                out.write(pre)
                out.write("class config:\n")
                out.write("  font_copyright = '{}'\n".format(self.copyright))
                out.write("  font_family = '{}'\n".format(self.family))
                out.write("  font_name = '{}'\n".format(self.name))
                out.write("  font_version = '{}'\n".format(self.version))
                out.write("\n")

                for icon_set_cls in utils.as_iterable(self.collections):
                    out.write("{}_opt = {}\n".format(icon_set_cls.__name__, icon_set_cls.options))
                out.write("\n")

                out.write("global_transform = {}\n".format(self.transformation or None))
                out.write("\n")

                out.write("output_formats = {}\n".format(self.output_formats or ('ttf',)))
                out.write("\n")

                out.write("verbose = {}\n".format(self.verbose))
                out.write("\n")

                out.write("select = [\n")
                for glyph in self.icons:
                    out.write("  ({}, '{}', r'{}', {}_opt),\n".format(hex(glyph.code), glyph.name, glyph.path.absolute(), glyph.source.__name__))
                out.write("]\n")
                out.write("\n")

                out.write("build_dir = r'{}'".format(env.BAWR_OUTPUT_DIR.absolute()))
                out.write(pos)

    def run(self, env):
        cache_dir = utils.get_cache_dir(env) 
        tool = FontForgeTool(env)
        tool(Path(cache_dir, '_ff_.py'))
