#!/usr/bin/env python

'''
Usage: supplemental-figures.py -i INPUT -o OUTPUT -v VARIABLES

Options:
    -i --input INPUT        Path to input YAML
    -o --output OUTPUT      Path to output markdown
    -v --var VARIABLES      Path to variables flatfile
'''

import yaml
from docopt import docopt

args = docopt(__doc__)

data = yaml.load(open(args['--input']))
variables = yaml.load(open(args['--var']))

output = '# Supplemental Figures\n\n'

if data['figures'] is not None:
    for i, figure in enumerate(data['figures']):
        figure_id = list(figure.keys())[0]
        figure_data = list(figure.values())[0]

        title = figure_data['title'].strip()[:-1] \
            if figure_data['title'].strip().endswith('.') \
            else figure_data['title']

        output += '![]({src})\n\n> **Supplementary Figure {index}. {title}.** {caption}\n\n\clearpage\n\n'.format(
            index = str(i + 1),
            title = title,
            caption = figure_data['caption'],
            src = figure_data['src']
        )

        variables['fig-' + str(figure_id) + '-idx'] = i + 1

with open(args['--output'], 'w') as outfile:
    outfile.write(output)

with open(args['--var'], 'w') as outfile:
    yaml.dump(variables, outfile, default_flow_style=False)
