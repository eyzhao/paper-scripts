#!/usr/bin/env python

"""
Pandoc filter to convert all level 2+ headers to paragraphs with
emphasized text.
"""

import panflute as pf

def is_title_line(elem):
    if len(elem.content) < 3:
        return False
    elif not all (isinstance(x, (pf.Str, pf.Space)) for x in elem.content):
        return False
    elif not (elem.content[0].text == '$chapter' or elem.content[0].text == '$unnumbered'):
        return False
    elif type(elem.content[1]) != pf.Space:
        return False
    else:
        return True

def get_title_name(elem):
    return(pf.stringify(elem, newlines=False).split(maxsplit=1)[1])

def action(elem, doc):
    if isinstance(elem, pf.Para) and is_title_line(elem):
        title = get_title_name(elem)
        chapter_elem = pf.Header(pf.Str(title))
        if elem.content[0].text == '$unnumbered':
            chapter_elem.classes = ['unnumbered']
        return chapter_elem
    elif type(elem) == pf.Header:
        elem.level += 1

def main(doc = None):
    return pf.run_filter(action, doc = doc)

if __name__ == "__main__":
    main()
