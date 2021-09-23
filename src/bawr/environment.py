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

import shutil
from pathlib import Path
import sys


def get_command_path(path, name):
    if not path:
        return Path(shutil.which(name))
    elif isinstance(path, str):
        return Path(path)


class Environment:
    FONTFORGE_PATH = None
    INKSCAPE_PATH = None
    BAWR_OUTPUT_DIR = None
    BAWR_SOURCE_DIR = None
    BAWR_CONFIG_FILE = None

    def build(self, cfg_file, src_dir, out_dir):
        self.FONTFORGE_PATH = get_command_path(self.FONTFORGE_PATH, 'fontforge')
        self.INKSCAPE_PATH = get_command_path(self.INKSCAPE_PATH, 'inkscape')

        if src_dir:
            self.BAWR_SOURCE_DIR = Path(src_dir)
        elif not self.BAWR_SOURCE_DIR:
            self.BAWR_SOURCE_DIR = Path('.')
        else:
            self.BAWR_SOURCE_DIR = Path(self.BAWR_SOURCE_DIR)

        if out_dir:
            self.BAWR_OUTPUT_DIR = Path(out_dir)
        elif not self.BAWR_OUTPUT_DIR:
            self.BAWR_OUTPUT_DIR = Path('.', 'build')
        else:
            self.BAWR_OUTPUT_DIR = Path(self.BAWR_OUTPUT_DIR)
            
        self.BAWR_CONFIG_FILE = Path(cfg_file)
        if not self.BAWR_CONFIG_FILE.exists():
            print(f"Configuration file not found: {cfg_file}")
            sys.exit(-1)

        for k, v in self.__dict__.items():
            print("ENV: {} = {}".format(k, v))
