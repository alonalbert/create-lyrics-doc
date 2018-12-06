#!/usr/bin/python
#
import sys
import lxml.etree as etree
import xml.etree.ElementTree as ET

from os import path


LINE_FORMAT = '            <text:p text:style-name="LINE">%s\n'
TRANSLATED_LINE_FORMAT = '                <text:span text:style-name="TRANSLATED_LINE">(%s)</text:span>\n'
CLOSE_LINE = '            </text:p>\n'
EMPTY_LINE = '            <text:p text:style-name="LINE"/>\n'

TITLE_LINE = 443
INSERTION_LINE = TITLE_LINE + 3
TRANSLATED_TITLE_LINE = TITLE_LINE + 1

NAMESPACES = {
  'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
  'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}


def stringify_children(node):
  from lxml.etree import tostring
  from itertools import chain
  parts = ([node.text] +
           list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) +
           [node.tail])
  # filter removes possible Nones in texts and tails
  return ''.join(filter(None, parts))


if __name__ == '__main__':
  filename = sys.argv[1]

  basename = path.basename(filename)
  dirname = path.dirname(filename)
  (name, ext) = path.splitext(basename)

  with open(filename) as f:
    originalLines = f.readlines()
  with open(path.join(dirname, name + '-translated' + ext)) as f:
    translatedLines = f.readlines()

  if len(originalLines) != len(translatedLines):
    print 'Line mismatch. Aborting'
    exit(1)

  with open(path.join(path.dirname(sys.argv[0]), 'template.xml')) as f:
    outputLines = f.readlines()

  outputLines[TITLE_LINE] = outputLines[TITLE_LINE].replace('Title', originalLines[0].strip())
  outputLines[TRANSLATED_TITLE_LINE] = outputLines[TRANSLATED_TITLE_LINE].replace('Translated title', translatedLines[0].strip())

  at = INSERTION_LINE
  for (i, line) in enumerate(originalLines[1:]):
    line = line.strip()
    if line == '':
      outputLines.insert(at, EMPTY_LINE)
      at += 1
    else:
      outputLines.insert(at, LINE_FORMAT % line)
      outputLines.insert(at + 1, TRANSLATED_LINE_FORMAT % translatedLines[i + 1].strip())
      outputLines.insert(at + 2, CLOSE_LINE)
      at += 3

  with open(path.join(dirname, name + '.odt'), 'w') as f:
    f.writelines(outputLines)

  with open(path.join(dirname, name + '.xml'), 'w') as f:
    f.writelines(outputLines)

