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

import argparse
from bawr import config_parser as cp

VERSION = '0.0.8'

def banner():
    print(r'''
  ______  ___  _    _______ 
  | ___ \/ _ \| |  | | ___ \
  | |_/ / /_\ \ |  | | |_/ /
  | ___ \  _  | |/\| |    / 
  | |_/ / | | \  /\  / |\ \ 
  \____/\_| |_/\/  \/\_| \_|

  version {}                          
  (c) Copyright 2021 Frank David Martinez Muñoz  
      Licensed under MIT License.

    '''.format(VERSION))


def main(args):
    banner()
    cfg = cp.Parser(args.cfg, dict(src_dir=args.src, out_dir=args.out))


def command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", help="Output directory path", default="build")
    parser.add_argument("--src", help="Source directory path", default=".")
    parser.add_argument("--cfg", help="Config file", default="config.py")
    return parser.parse_args()


if __name__ == '__main__':
    main(command_line_arguments())
