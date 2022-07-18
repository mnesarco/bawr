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
from bawr.glyph import Glyph
from bawr.tool_inkscape import InkscapeTool
from bawr import utils
import os

try:
    from PIL import Image
except:
    Image = None

try:
    from rectpack.packer import SORT_AREA, PackingBin, PackingMode, MaxRectsBssf
    from rectpack import newPacker
except:
    newPacker = None


def pack(cells, width, height):
    packer = newPacker(
        mode=PackingMode.Offline, 
        bin_algo=PackingBin.BBF, 
        pack_algo=MaxRectsBssf, 
        sort_algo=SORT_AREA, 
        rotation=False
    )
    for i, cell in enumerate(cells):
        packer.add_rect(cell.width, cell.height, rid=i)
    packer.add_bin(width, height)
    packer.pack()
    for bin in packer:
        for rect in bin:
            cells[rect.rid].x = rect.left
            cells[rect.rid].y = rect.top - rect.height


class Cell:
    def __init__(self, file, name, size, margin):
        self.file = file
        self.name = name
        self.width = size
        self.height = size
        self.x = 0
        self.y = 0
        self.margin = margin


class Atlas:

    # Config
    name = 'atlas'
    collections = []
    width = 512
    sizes = (16, 32, 64)

    # Generated
    height = 0
    icons = []
    cells = []
    instance = None
    output = None

    def build(self, env):
        print("[Atlas Texture] Start ...")

        self.icons = []
        self.cells = []

        if not env.INKSCAPE_PATH:
            print("[Atlas Texture] Cancelled: Inkscape not available.")
            return

        if not Image:
            print("[Atlas Texture] Cancelled: Pillow not available.")
            return

        if not newPacker:
            print("[Atlas Texture] Cancelled: Reckpack not available")
            return

        code = 0
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
                    print("[Atlas Texture] Invalid source dir: {}".format(source.absolute()))
        self.generate_individual_cells(env)
        self.generate_texture(env)
        print("[Atlas Texture] {}".format(self.output))


    def generate_individual_cells(self, env):     
        cache_dir = utils.get_cache_dir(env) 
        inkscape = InkscapeTool(env)          
        for glyph in self.icons:
            file = glyph.path
            margin = 0

            if glyph.source.options:
                processors = glyph.source.options.get('atlas_preprocessors', [])
                margin = glyph.source.options.get('atlas_margin', 0)
                for p in processors:
                    file = p(env, file, glyph.source.__name__)
            
            if margin > 1:
                margin = 1.0 / margin
            elif margin == 1:
                margin = 0
            elif margin < 0:
                margin = 0
            
            for size in self.sizes:
                png = Path(cache_dir, "{}_{}_{}.png".format(glyph.source.__name__, file.stem, size))
                if (not png.exists()) or png.stat().st_mtime < file.stat().st_mtime:
                    inkscape(file, png, size, int(margin * size))
                self.cells.append(Cell(png, glyph.name, size, int(margin * size)))

        pack(self.cells, self.width, self.width * 20)


    def generate_texture(self, env):
        height = 0
        for cell in self.cells:
            h = cell.y + cell.height
            if h > height:
                height = h
        atlas = Image.new("RGBA", (self.width, height))
        for cell in self.cells:
            self.apply_image(cell, cell.margin, atlas)
        self.output = Path(env.BAWR_OUTPUT_DIR, (self.name or 'atlas') + '.png')
        atlas.save(self.output, quality=99, optimize=True)
        self.height = height


    def apply_image(self, cell, margin, atlas):
        icon = Image.open(cell.file)
        pos = (cell.x, cell.y)
        if margin > 0:
            pos = (pos[0] + margin, pos[1] + margin) 
        atlas.paste(icon, pos)


