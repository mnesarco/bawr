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

import os
import sys
import ast
import importlib
import shutil
from pathlib import Path
from bawr.environment import Environment
from bawr import utils


def load_config_file(path):
    with open(path, 'r') as f:
        return ast.parse(f.read())


class Analyzer(ast.NodeVisitor):
    BUILDER_REGISTRY = ('Font', 'Atlas', 'CppFontHeader', 'CppEmbedded', 'ImGuiFontLoader', 'CppAtlasHeader')

    def __init__(self):
        super().__init__()
        self.iconsets = dict()
        self.builders = dict()
        self.env = None

    def visit_ClassDef(self, node):
        for base in node.bases:
            kind = base.id
            if kind in Analyzer.BUILDER_REGISTRY:
                self.builders[node.name] = (kind, None)
            elif kind == 'IconSet':
                self.iconsets[node.name] = None
            elif kind == 'Environment':
                if self.env is not None:
                    print("[Error] Only one environment definition is allowed: line {}".format(node.lineno))
                    exit(-1)
                self.env = node.name


class Parser:
    data = None
    analyzer = None
    env = None

    def __init__(self, source, args):
        self._parse(source)
        self._environment(source, args['src_dir'], args['out_dir'])
        self._clean()
        self._prepare()
        self._iconsets()
        self._builders()
        self._end()

    def _parse(self, source):
        path = Path(source)
        analyzer = Analyzer()
        analyzer.visit(load_config_file(path))
        self.data = importlib.import_module(path.stem, source)
        self.analyzer = analyzer

    def _environment(self, cfg_file, src_dir, out_dir):
        print("_" * 80)
        if self.analyzer.env:
            ctor = getattr(self.data, self.analyzer.env)
        else:
            ctor = Environment
        self.env = ctor()
        self.env.build(cfg_file, src_dir, out_dir)

    def _prepare(self):
        try:
            if not self.env.BAWR_OUTPUT_DIR.exists():
                os.mkdir(self.env.BAWR_OUTPUT_DIR)
        except:
            sys.exit("Error creating output directory: %s" % self.env.BAWR_OUTPUT_DIR)   

    def _iconsets(self):
        print("_" * 80)
        for iconset in self.analyzer.iconsets:
            ctor = getattr(self.data, iconset)
            inst = ctor()
            inst.build(self.env)
            ctor.instance = inst

    def _builders(self):
        for builder in self.analyzer.builders:
            print("_" * 80)
            ctor = getattr(self.data, builder)
            inst = ctor()
            inst.build(self.env)
            ctor.instance = inst

    def _clean(self):
        cache_dir = utils.get_cache_dir(self.env)
        witness = Path(cache_dir, "__cfg__")
        if not witness.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
        else:
            if witness.stat().st_mtime < self.env.BAWR_CONFIG_FILE.stat().st_mtime:
                shutil.rmtree(cache_dir, ignore_errors=True)

    def _end(self):
        cache_dir = utils.get_cache_dir(self.env)
        witness = Path(cache_dir, "__cfg__")
        with open(witness, 'w') as f:
            f.write(f"{self.env.BAWR_CONFIG_FILE}")