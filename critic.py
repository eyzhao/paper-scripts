#!/usr/bin/env python

"""
Pandoc filter to enable CriticMarkdown.
"""

import panflute as pf
import sys

def debug(*args, **kwargs):
    """
    Same as print, but prints to ``stderr``
    (which is not intercepted by Pandoc).
    """
    print(file=sys.stderr, *args, **kwargs)

def prepare(doc):
    doc.critic_mode = doc.get_metadata()['critic-mode']

def action(elem, doc):
    if type(elem) == pf.Strikeout:
        raw_text = pf.stringify(elem)
        if '>>' in raw_text \
                or (raw_text.startswith('++') and raw_text.endswith('++')) \
                or (raw_text.startswith('--') and raw_text.endswith('--')):
            if '>>' in raw_text:
                text_split = raw_text.split('>>')

                if doc.critic_mode == 'original':
                    new_text = pf.convert_text(text_split[0])
                elif doc.critic_mode == 'edited':
                    new_text = pf.convert_text(text_split[1])
                else:
                    new_text = pf.convert_text('~~' + text_split[0] + '~~\\uline{' + text_split[1] + '}')

            elif raw_text.startswith('++'):
                text_split = ['', raw_text[2:-2]]

                if doc.critic_mode == 'original':
                    new_text = pf.convert_text(text_split[0])
                elif doc.critic_mode == 'edited':
                    new_text = pf.convert_text(text_split[1])
                else:
                    return(pf.RawInline('\\uline{' + text_split[1] + '}', format='latex'))

            elif raw_text.startswith('--'):
                text_split = [raw_text[2:-2], '']

                if doc.critic_mode == 'original':
                    new_text = pf.convert_text(text_split[0])
                elif doc.critic_mode == 'edited':
                    new_text = pf.convert_text(text_split[1])
                else:
                    new_text = pf.convert_text('~~' + text_split[0] + '~~')


            if len(new_text) == 0:
                return pf.convert_text('')
            else:
                return(list(new_text[0].content))

def main(doc = None):
    return pf.run_filter(action, doc = doc, prepare = prepare)

if __name__ == "__main__":
    main()
