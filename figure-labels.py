#!/usr/bin/env python

''' Figure Labels

Usage: figure-labels.py -i INPUT

Options:
    -i --input INPUT            Input Markdown File
'''

from __future__ import print_function
from docopt import docopt
import re

args = docopt(__doc__)

r = re.compile(r'\!\[(.*?)\]\((.*?)\)\{(.*?)\}')

input_path = args['--input']
markdown = open(input_path)

for line in markdown:
    match = r.findall(line)
    if len(match) == 1:
        m = match[0]
        print(line)
        print("> Figure {{{0}}}: {1}".format(m[2].replace('#', '@'),
                                           m[0]),
              end = '')
    else:
        print(line, end = '')
