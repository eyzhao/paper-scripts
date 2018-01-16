#!/usr/bin/env python

''' Markdown Variables

Usage: markdown-variables.py -i INPUT -v VARIABLES [ --boldface ]

Options:
    -i --input INPUT            Input Markdown File
    -v --variables VARIABLES    Key-value config file with variables and their values separated by "=" sign
    --boldface                  Boldface the markdown variables in text for easier identification
'''

from docopt import docopt
import yaml
import re
import warnings

args = docopt(__doc__)

input_file = open(args['--input']).read()

variables = yaml.load(open(args['--variables']))

for key, value in variables.items():
    key = str(key)
    value = str(value)
    if key.strip():
        if args['--boldface']:
            value = '**' + value.strip() + '**'
        input_file = input_file.replace('{@var:' + key.strip() + '}', value.strip())

var_re = re.compile(r'{@var:.*?}')
remaining_variables = set(m.replace('{@var:', '').replace('}', '') for m in var_re.findall(input_file))

for variable in remaining_variables:
    warnings.warn('Unmatched variable: {}'.format(variable))

print(input_file)
