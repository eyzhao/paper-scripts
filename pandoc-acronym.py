#!/usr/bin/env python

'''
'''

from pandocfilters import *

used_acronyms = set()

def get_value(acronym, suffix, option, acronym_dictionary):
    # option may be either 'short' or 'full' or 'both'
    if not option in ('short', 'both', 'full'):
        option = 'short'

    d = open(acronym_dictionary)
    for line in d:
        (key, value) = [x.strip() for x in line.split('=')]
        if key == acronym:
            if option == 'full':
                return value + suffix
            elif option == 'both':
                return '{0}{2} ({1}{2})'.format(value, key, suffix)
            else:
                return key + suffix

    raise AcronymError('No value exists for acronym: {0}'.format(acronym))

def test(key, value, format, meta):
    global used_acronyms

    if key == 'Para':
        acronym_indices = [
                i for i in range(0, len(value))
                if value[i]['t'] == 'Str'
                and '[+' in value[i]['c']
                and ']' in value[i]['c']
        ]

        for idx in acronym_indices:
            item = value[idx]

            acronym_content = item['c']
            acronym_value = acronym_content.split('[+')[1].split(']')[0]
            acronym_code = acronym_value.split(':')
            acronym = acronym_code[0].strip()

            if acronym in used_acronyms:
                acronym_type = 'short'
            else:
                acronym_type = 'both'

            suffix = acronym_code[1].strip() if len(acronym_code) >= 2 else ''
            option = acronym_code[2].strip() if len(acronym_code) >= 3 else acronym_type

            used_acronyms.add(acronym)

            acronym_output = get_value(acronym, suffix, option, meta['acronyms']['c'][0]['c'])

            try:
                return_string = acronym_content.replace('[+' + acronym_value + ']', acronym_output)
                value[idx]['c'] = return_string
            except:
                raise AcronymError('Acronym parsing failed for acronym: {0}. Acronym value was {1}. Acronym output was {2}.'.format(acronym_content, acronym_value, acronym_output))

        return(Para(value))

class AcronymError(Exception):
    pass

if __name__ == '__main__':
    toJSONFilter(test)
