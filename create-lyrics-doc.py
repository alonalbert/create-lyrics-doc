#!/usr/bin/python
#
import sys

from os import path


LINE_FORMAT = '            <text:p text:style-name="LINE">%s\n'
TRANSLATED_LINE_FORMAT = '                <text:span text:style-name="TRANSLATED_LINE">(%s)</text:span>\n'
CLOSE_LINE = '            </text:p>\n'
EMPTY_LINE = '            <text:p text:style-name="LINE"/>\n'

TITLE_LINE = 443
INSERTION_LINE = TITLE_LINE + 3
TRANSLATED_TITLE_LINE = TITLE_LINE + 1

if __name__ == '__main__':
  dir = sys.argv[1]
  name = path.basename(dir)

  with open(path.join(dir, "original.txt")) as f:
    originalLines = f.readlines()
  with open(path.join(dir, "translated.txt")) as f:
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

  with open(path.join(dir, name + '.odt'), 'w') as f:
    f.writelines(outputLines)
