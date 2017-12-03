#!/usr/bin/env python

''' Markdown Variables

Usage: markdown-variables.py -i INPUT -v VARIABLES [ --boldface ]

Options:
    -i --input INPUT            Input Markdown File
    -v --variables VARIABLES    Key-value config file with variables and their values separated by "=" sign
    --boldface                  Boldface the markdown variables in text for easier identification
'''

from docopt import docopt

args = docopt(__doc__)

input_file = open(args['--input']).read()
variables_file = open(args['--variables'])

variables = {line.split('=')[0].strip() : line.split('=')[1].strip() for line in variables_file
             if '=' in line and not line.startswith('#')}

for key, value in variables.items():
    if key.strip():
        if args['--boldface']:
            value = '**' + value.strip() + '**'
        input_file = input_file.replace('{@var:' + key.strip() + '}', value.strip())


print(input_file)
