#!/usr/bin/env python

''' pandoc-acronym.py

A Pandoc filter that introduces acronym handling.

Usage: pandoc -o <output> --filter=path/to/pandoc-acronym.py <input>

In the <input> document, use the syntax [+KEY]. In a separate <acronyms> file
write

KEY = FULL_VALUE

with one acronym per line.

When running pandoc-acronym.py filter, the first instance of [+KEY] will be replaced
automatically with FULL_VALUE (KEY). All subsequent instances will, by default,
be replaced with KEY automatically.

The general form of the in-text statement is [+KEY:<suffix>:<capitalization>:<option>].
- <suffix> can take on any value.
- <capitalization> can take on values "upperstart" or "lower"
- <option> can take on values "short", "full", or "both" (without the quotes).

If you want to add a suffix (i.e. to pluralize an acronym), add the suffix after a colon,
as follows: [+KEY:s]. This will be replaced with either FULL_VALUEs (KEYs) or with KEYs
depending on the previously stated pattern.

If you want to force a value to write out in full, use [+KEY:<suffix>:full]. This writes
FULL_VALUE<suffix>. If you want to force a restatement of the acronym, use [+KEY:<suffix>:both],
which writes FULL_VALUE<suffix> (KEY<suffix>). To force usage of the acronym, use
[+KEY:<suffix>:short].
'''

from pandocfilters import *

used_acronyms = set()

def debug(*args, **kwargs):
    """
    Same as print, but prints to ``stderr``
    (which is not intercepted by Pandoc).
    """
    print(file=sys.stderr, *args, **kwargs)


def get_value(acronym, suffix, capitalization, option, acronym_dictionary):
    # option may be either 'short' or 'full' or 'both'
    if not option in ('short', 'both', 'full'):
        option = 'short'

    if not capitalization in ('upperstart', 'lower', 'default'):
        capitalization = 'default'

    d = open(acronym_dictionary)
    for line in d:
        (key, value) = [x.strip() for x in line.split('=')]

        if key == acronym:
            if capitalization == 'lower':
                value = value.lower()
            elif capitalization == 'upperstart':
                value = value[0].upper() + value[1:]

            if option == 'full':
                out = value + suffix
            elif option == 'both':
                out = '{0}{2} ({1}{2})'.format(value, key, suffix)
            else:
                out = key + suffix

            return out

    raise AcronymError('No value exists for acronym: {0}'.format(acronym))

def test(key, value, format, meta):
    global used_acronyms

    if key == 'Para' or key == 'Strikeout':
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
            capitalization = acronym_code[2].strip() if len(acronym_code) >= 3 else ''
            option = acronym_code[3].strip() if len(acronym_code) >= 4 else acronym_type

            used_acronyms.add(acronym)

            acronym_output = get_value(acronym, suffix, capitalization, option, meta['acronyms']['c'][0]['c'])

            try:
                return_string = acronym_content.replace('[+' + acronym_value + ']', acronym_output)
                value[idx]['c'] = return_string
            except:
                raise AcronymError('Acronym parsing failed for acronym: {0}. Acronym value was {1}. Acronym output was {2}.'.format(acronym_content, acronym_value, acronym_output))

        if key == 'Para':
            return(Para(value))
        elif key == 'Strikeout':
            return(Strikeout(value))

class AcronymError(Exception):
    pass

if __name__ == '__main__':
    toJSONFilter(test)
