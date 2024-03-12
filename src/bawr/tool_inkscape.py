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

import subprocess
import sys
import shlex

class InkscapeTool:

    def __init__(self, env):
        self.env = env

    def __call__(self, svg_file, png_file, size, margin=0):
        if margin > 0:
            size -= 2*margin

        cmd_exec =  [
            str(self.env.INKSCAPE_PATH),
            '--export-background-opacity=0',
            f'--export-width={size}',
            '--export-type=png',
            '-o', str(png_file), 
            str(svg_file)
        ]
        print(f"[EXEC] {shlex.join(cmd_exec)}")
        process = subprocess.Popen(cmd_exec, shell=False)
        try:
            err = process.wait(30)
            if (err):
                sys.exit(f"Error: Inkscape terminated with status = {err}")
        except subprocess.TimeoutExpired:
            sys.exit(f"Error: Inkscape timeout")
