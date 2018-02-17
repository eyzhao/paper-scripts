#!/usr/bin/env python

"""
Panflute filter to allow variable substitution
"""

import yaml
import re
import warnings
import panflute as pf
import sys

match_key = re.compile(r'\{\?var:(.*?)\}')

def prepare(doc):
    doc.variables = yaml.load(open(doc.get_metadata('variables', default='variables.yml')))
    doc.boldface_variables = doc.get_metadata('boldface_variables', default=False)

    doc.var_re = re.compile(r'\{?var:(.*?)\}')
    doc.missing_variables = set([])

def action(elem, doc):
    if type(elem) == pf.Str:
        if len(match_key.findall(elem.text)) > 0:
            var_key = match_key.findall(elem.text)[0]

            if var_key in doc.variables:
                if doc.boldface_variables:
                    var_value = pf.Strong(pf.Str(str(doc.variables[var_key])))
                else:
                    var_value = pf.Str(str(doc.variables[var_key]))
            else:
                var_value = pf.Strong(pf.Str('{{Missing variable: {}}}'.format(var_key)))
                doc.missing_variables.add(var_key)

            return(var_value)

def finalize(doc):
    for variable in doc.missing_variables:
        warnings.warn('Unmatched variable: {}'.format(variable))

def main(doc=None):
    return pf.run_filter(action, prepare=prepare, finalize=finalize, doc=doc)

if __name__ == '__main__':
    main()
