#!/usr/bin/python
#
import sys

from os import path, listdir
from shutil import copyfile

LINK_FORMAT = '<a class="link" href="{0}">{1}</a><br/>\n'
TITLE_FORMAT = '<span class="title" onload="load(this)" onclick="toggle(this)" data-text="{0}" data-translation="{1}">{0}</span>\n'
LINE_FORMAT = '<div class="line" onload="load(this)" onclick="toggle(this)" data-text="{0}" data-translation="{1}">{0}</div>\n'
EMPTY_LINE = '<br/>\n'

COPY_FILES = [
  'lyrics.css',
  'lyrics.js',
  'lyrics.png',
]

def find(lines, text):
  for (i, line) in enumerate(lines):
    if (text in line):
      return i + 1

if __name__ == '__main__':
  siteDir = path.join(path.dirname(sys.argv[0]), 'site')

  src = sys.argv[1]
  dst = sys.argv[2]

  links = []
  for song in sorted(listdir(src)):
    dir = path.join(src, song)

    with open(path.join(dir, "original.txt")) as f:
      originalLines = f.readlines()
    with open(path.join(dir, "translated.txt")) as f:
      translatedLines = f.readlines()

    if len(originalLines) != len(translatedLines):
      print 'Line mismatch. Aborting'
      exit(1)

    with open(path.join(siteDir, 'lyrics.html')) as f:
      lines = f.readlines()


    at =  find(lines, '<div id="header">')

    lines.insert(at, TITLE_FORMAT.format(originalLines[0], translatedLines[0]))
    at =  find(lines, '<div id="content">')
    maxLine = 0
    for (i, line) in enumerate(originalLines[1:]):
      line = line.strip()
      if len(line) > maxLine:
        maxLine = len(line)

      if line == '':
        lines.insert(at, EMPTY_LINE)
      else:
        translatedLine = translatedLines[i + 1].strip()
        if len(translatedLine) > maxLine:
          maxLine = len(translatedLine)
        lines.insert(at, LINE_FORMAT.format(line, translatedLine))
      at += 1


    htmlFilename = song.replace(' ', "_").lower() + '.html'
    links += LINK_FORMAT.format(htmlFilename, song)
    with open(path.join(dst, htmlFilename), 'w') as f:
      f.writelines(lines)

    for file in COPY_FILES:
      copyfile(path.join(siteDir, file), path.join(dst, file))

  with open(path.join(siteDir, 'lyrics.html')) as f:
    indexLines = f.readlines()

  at = find(indexLines, '<body>')
  for link in links:
    indexLines.insert(at, link)
    at += 1

  with open(path.join(dst, 'index.html'), 'w') as f:
    f.writelines(indexLines)
