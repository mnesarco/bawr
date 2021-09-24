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
import re
import os

RE_VAR = re.compile(r'\$\{(.*?)\}')

class CppEmbedded:

    # Config
    name = None
    namespace = None
    source = None

    # Generated
    instance = None
    output_data = None
    output_header = None

    def build(self, env):
        print("[Cpp Bin Embedder] Start ...")

        def replacer(match):
            return str(getattr(env, match.group(1), match.group(1)))

        input_bin = Path(RE_VAR.sub(replacer, self.source).replace('/', os.sep).replace('\\', os.sep))
        name = self.name if self.name else input_bin.stem
        self.name = name

        self.output_data = Path(env.BAWR_OUTPUT_DIR, name + ".cpp")
        self.output_header = Path(env.BAWR_OUTPUT_DIR, name + ".hpp")

        utils.bin_to_cpp_data(
            self.output_data, 
            self.namespace or 'icons', 
            input_bin
        )

