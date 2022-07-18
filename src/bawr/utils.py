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

import re
import struct
import os
from pathlib import Path
from collections.abc import Iterable

class StringReplacer:
    '''
    table = {
        "aaa"    : "[This is three a]",
        "b+"     : "[This is one or more b]",
        r"<\w+>" : "[This is a tag]"
    }
    replacer = StringReplacer(table, True)
    sample1 = "whatever bb, aaa, <star> BBB <end>"
    print(replacer(sample1))
    >> whatever [This is one or more b], [This is three a], [This is a tag] [This is one or more b] [This is a tag]
    '''
    def __init__(self, replacements, ignore_case=False):
        patterns = sorted(replacements, key=len, reverse=True)
        self.replacements = [replacements[k] for k in patterns]
        re_mode = re.IGNORECASE if ignore_case else 0
        self.pattern = re.compile('|'.join(("({})".format(p) for p in patterns)), re_mode)
        self.changed = False
        def tr(matcher):
            self.changed = True
            index = next((index for index,value in enumerate(matcher.groups()) if value), None)
            return self.replacements[index]
        self.tr = tr

    def __call__(self, string):
        self.changed = False
        return self.pattern.sub(self.tr, string)


def bin_to_cpp_data(cpp_file, namespace, bin_file, data_var='DATA', size_var='SIZE', sub_namespace='data'):

    if not bin_file.exists():
        print(f"[Cpp Bin Embedder] Bin file not found: {bin_file}\n")
        return   

    hpp_file = Path(cpp_file.parent, cpp_file.stem + ".hpp")
    print(f"[Cpp Bin Embedder] < {bin_file}")
    print(f"[Cpp Bin Embedder] > {cpp_file}")
    print(f"[Cpp Bin Embedder] > {hpp_file}")

    padding = [None, b"\x00", b"\x00\x00", b"\x00\x00\x00"]
    with open(hpp_file, 'w') as f:
        f.write("#pragma once\n\n")
        f.write(f"namespace {namespace} {{\n")
        f.write(f" namespace {sub_namespace} {{\n")
        f.write(f"  extern const unsigned int {size_var};\n")
        f.write(f"  extern const unsigned int {data_var}[];\n")
        f.write(" }\n")
        f.write("}\n")

    with open(cpp_file, 'w') as f:
        f.write(f'#include "{hpp_file.name}"\n')
        f.write(f"namespace {namespace} {{\n")
        f.write(f" namespace {sub_namespace} {{\n")
        f.write(f"  const unsigned int {size_var} = {os.stat(bin_file).st_size};\n")
        f.write(f"  const unsigned int {data_var}[] = {{\n  ")
        with open(bin_file, 'rb') as bin:
            n = 0
            c = bin.read(4)
            while (c):
                val = struct.unpack("<L", c)[0]
                f.write(f"{val:#010x}")
                f.write(",")
                n += 1
                if n % 12 == 0:
                    f.write("\n  ")
                c = bin.read(4)
                missing = 4 - len(c)
                if missing > 0 and missing < 4:
                    c += padding[missing]
        f.write("};\n")
        f.write(" }\n")
        f.write("}\n")

def get_cache_dir(env):
    path = Path(env.BAWR_OUTPUT_DIR, "__bawr_cache__")
    if not path.exists():
        os.makedirs(path, exist_ok=True)
    return path

def as_iterable(obj):
    if isinstance(obj, Iterable):
        return obj
    return (obj,)
