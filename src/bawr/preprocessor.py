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

from bawr import utils
from pathlib import Path 
import hashlib

class RegexReplacePreprocessor:

    def __init__(self, translations, ignore_case = True):
        self.translations = translations
        self.ignore_case = ignore_case
        self.processor = utils.StringReplacer(translations, ignore_case)

    def __call__(self, env, file, iconset):
        name = hashlib.sha256("{}{}{}".format(self.__class__.__name__, iconset, file.stem).encode()).hexdigest()
        cache_dir = utils.get_cache_dir(env)
        path = Path(cache_dir, "{}.svg".format(name))
        if path.exists() and path.stat().st_mtime > file.stat().st_mtime:
            return path
        with open(file, mode='r') as f:
            txt = f.read()
            txt = self.processor(txt)
            if self.processor.changed:
                with open(path, mode="w") as w:
                    w.write(self.processor(txt))
                    return path
        return file

    def __repr__(self):
        return "{}"

