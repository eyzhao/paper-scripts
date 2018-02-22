#!/usr/bin/env python

''' list-of-acronyms.py

Usage: list-of-acronyms.py -i INPUT

Options:
    -i --input INPUT        Path to file where each line contains an acronym and
                            the full phrase, separated by an equals (=) sign.
                            Any whitespace padding will be ignored. Redundant
                            acronyms will be collapsed.
'''

from warnings import warn
from docopt import docopt

args = docopt(__doc__)

acronyms_file = open(args['--input'])

acronyms = {}
for line in acronyms_file:
    split = line.split('=')
    key = split[0].strip()
    value = split[1].strip()

    if key in acronyms:
        if value != acronyms[key]:
            warn('Conflicting values assigned to acronym: {}. Values are {} and {}'.format(
                key, value, acronyms[key]
            ))

    acronyms[key] = value

output = ''
for key,value in acronyms.items():
    output += r'\nomenclature{' + key + '}{' + value + '}\n'

print(output)
