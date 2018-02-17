''' short-captions.py

Automatically builds short captions from the first sentence of captions.

Usage: cat INPUT | python short-captions.py
'''

import re
import sys

input = sys.stdin.read()

match_string = r'\\caption\{.*?\.[\s}]'
caption_string = r'\\caption\{(.*?)\.[\s}]'

matches = re.findall(match_string, input, flags=re.DOTALL)
shortcaptions = re.findall(caption_string, input, flags=re.DOTALL)

shortcaptions = [
    s.replace('\\', '').replace('textbf', '').replace('{', '').replace('}', '').replace('\n', ' ').replace('emph', '').replace('_', '\\_')
    for s in shortcaptions
]

for i, match in enumerate(matches):
    result = match.replace('\\caption', '\\caption[' + shortcaptions[i] + ']')
    input = input.replace(match, result)

print(input)
