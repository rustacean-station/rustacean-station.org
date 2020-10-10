#!/usr/bin/python3

"""

This is a tool for performing error checks on a transcript.

It performs the following checks:
- Make sure the front matter is present and is correctly formatted
- Flag places with more than one space in a row

It can perform the following "fixups":
- Change "--" to "—" (U+2014 EM DASH) (excluding `code segments`)
- Drop whitespace at the end of lines
- Re-flow the text, with care not to break up `code segments`

"""

import argparse
from itertools import islice
import os
import re
import string
from textwrap import wrap

COMMON_NON_ASCII = set(['—'])

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def split_front_matter(txt):
    """ return the input text split into two parts

    returns (front_matter, everything_else)
    """
    divider = '---\n'
    first = txt.find(divider)
    if first < 0:
        return ('', txt)
    second = txt.find(divider, first+4)
    if second < 0:
        return ('', txt)
    cut_point = second + len(divider)
    return (txt[:cut_point], txt[cut_point:])

def front_matter_check(txt):
    """ returns a list of errors in the front matter

    Well-formed front matter looks like this:
    ---
    title: "Blah blah blah"
    file: <some url>
    ---
    """
    result = []
    # Only inspect the first 4 nonempty lines
    lines = list(take(10, filter(lambda x: x.strip(), txt.splitlines())))

    if lines[0] != ('---'):
        result.append('Front matter missing? Missing "---"')
    else:
        if not re.match('title: ".*"$', lines[1]):
            result.append('Missing or malformed "title" line in front matter')
        if not re.match(r'file: http\S+$', lines[2]):
            result.append('Missing or malformed "file" line in front matter')
        if lines[3] != '---':
            result.append('Front matter missing trailing "---"')
    return result

def snip_window(line, offset):
    """ grab a 30-character window around a particular offset """
    snip_end = min(len(line), offset + 15)
    snip_start = max(0, snip_end - 30)
    if snip_start == 0:
        snip_end = 30
    return line[snip_start:snip_end]

def formatting_check(txt):
    result = []
    for linenum, line in enumerate(txt.splitlines()):
        if "  " in line:
            location = line.find("  ")
            snippet = snip_window(line, location)
            result.append('Line {} contains multiple spaces: "{}"'.format(linenum + 1, snippet))
        for location, c in enumerate(line):
            if c not in string.printable and c not in COMMON_NON_ASCII:
                snippet = snip_window(line, location)
                result.append('Line {} contains non-ascii character {}: "{}"'.format(
                    linenum + 1,
                    hex(ord(c)),
                    snippet))
        if '\t' in line:
            result.append('Line {} contains tab characters'.format(linenum + 1))
    return result

def munge_code(txt, old, new):
    """ replace one character with another, inside code blocks """
    chunks = txt.split('`')
    # An even number of ` characters means an odd number of chunks
    if len(chunks) % 2 == 0:
        raise Exception("confusing number of ` characters")
    result = ''
    for chunk_num, chunk in enumerate(chunks):
        if chunk_num % 2:
            result += '`' + chunk.replace(old, new) + '`'
        else:
            result += chunk
    return result

def split_paragraphs(txt):
    """ split txt at blank lines

    Also drops leading or trailing whitespace from each line.
    """
    result = ['']
    for line in txt.splitlines():
        line = line.strip()
        if result[-1]:
            if line == '':
                # Start a new paragraph
                result.append('')
                continue
            result[-1] += ' '
        result[-1] += line
    if not result[-1]:
        result = result[:-1]
    return result

def reflow(txt, width=80):
    # Remove the front matter before any processing.
    front_matter, txt = split_front_matter(txt)

    # Seek out `code` tags and replace spaces with temporary markers to prevent
    # breaking them up.
    txt = munge_code(txt, ' ', '␣')

    # Assemble a list of paragraphs (undoing any previous wrapping/reflow)
    paragraphs = split_paragraphs(txt)

    # Do the wrapping
    reflowed_para = []
    for p in paragraphs:
        assert type(p) is str
        new_p = wrap(p, width=width, replace_whitespace=True, drop_whitespace=True)
        reflowed_para.append('\n'.join(new_p))
    paragraphs = reflowed_para

    # Re-assemble the text
    result = '\n\n'.join(paragraphs)

    # Remove the code tag temporary markers
    result = munge_code(result, '␣', ' ')

    return front_matter + '\n' + result + '\n'

def emdashify(txt, width=80):
    """ replace '--' with em-dash '—', except in front matter or `code` """

    # Remove the front matter before any processing.
    front_matter, txt = split_front_matter(txt)

    # Seek out `code` tags and replace dashes with temporary markers to prevent
    # accidental damage.
    txt = munge_code(txt, '-', '┄')

    txt = txt.replace('--', '—')

    # switch code dashes back
    txt = munge_code(txt, '┄', '-')

    return front_matter + txt

def style_names(txt):
    """ replace 'Name: ' with '__Name__: ' """

    # match "Name: ", "Name Name: ", or "Name Name Name: "
    name_finder = re.compile(r'([\w\-]+(?: [\w\-]+){0,2}): (.*)')

    # Remove the front matter before any processing.
    front_matter, txt = split_front_matter(txt)

    result = ''
    armed = True
    for line in txt.splitlines():
        if line.strip() == '':
            armed = True
        elif armed:
            armed = False
            m = name_finder.match(line)
            if m and line[0].isupper():
                result += '__{}__: {}\n'.format(m.group(1), m.group(2))
                continue
        result += line + '\n'
    return front_matter + result

def write_and_rename(txt, target_filename):
    """ write into a temporary file, and then move it to the final location

    This write-and-move strategy helps avoid problems if we crash or are
    halted halfway through the write.  Writing to the same target directory
    makes the move atomic on most systems (because we'll be in the same
    filesystem).
    """
    tmp_name = target_filename + '.tmp'
    with open(tmp_name, 'w') as f:
        f.write(txt)
    os.replace(tmp_name, target_filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('check', 'fix'))
    parser.add_argument('--emdash', action='store_true')
    parser.add_argument('--reflow', action='store_true')
    parser.add_argument('--style-names', action='store_true')
    parser.add_argument('file')
    args = parser.parse_args()
    txt = open(args.file).read()
    if args.action == 'check':
        result = []
        result.extend(front_matter_check(txt))
        result.extend(formatting_check(txt))
        if result:
            print('\n'.join(result))
        else:
            print('SUCCESS')
    if args.action == 'fix':
        if args.style_names:
            txt = style_names(txt)
        if args.emdash:
            txt = emdashify(txt)
        if args.reflow:
            txt = reflow(txt)
        write_and_rename(txt, args.file)
