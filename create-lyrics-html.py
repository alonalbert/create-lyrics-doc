#!/usr/bin/python
# coding=utf-8

import sys
import json
from os import path, listdir
from shutil import copyfile
import copy
from gmusicapi.clients import Mobileclient
import unidecode

NEXT_FILE = '{next-file}'
NEXT_NAME = '{next-name}'
PREVIOUS_FILE = '{previous-file}'
PREVIOUS_NAME = '{previous-name}'

LINK_FORMAT = '<a class="link" href="{0}">{1}</a><br/>\n'
TITLE_FORMAT = '        <div class="title" onload="load(this)" onclick="toggle(this)" data-text="{0}" data-translation="{1}">{0}</div>\n'
LINE_FORMAT = '        <div class="line" onload="load(this)" onclick="toggle(this)" data-text="{0}" data-translation="{1}">{0}</div>\n'
EMPTY_LINE = '        <br/>\n'

COPY_FILES = [
  'lyrics.css',
  'lyrics.js',
  'lyrics.png',
]
EXTERNAL_TRACKS = {
  '8bdaec69-75e3-3ff7-8d14-a0f9eb9702a3': 'Duele el corazón',
  '02734350-569a-38f2-9678-4302a092ccc3': 'Negro y Azul',
}


def find(lines, text):
  for (i, line) in enumerate(lines):
    if (text in line):
      return i + 1


def toHtmlFileName(song):
  return song.replace(' ', "_").lower() + '.html'


def get_playlist_tracks(mc, name):
  playlists = mc.get_all_user_playlist_contents()
  tracks = []
  for playlist in playlists:
    if playlist['name'] == name:
      for track in playlist['tracks']:
        if track['source'] == '2':
          trackName = track['track']['title']
        else:
          trackName = EXTERNAL_TRACKS[track['trackId']].decode('utf-8')
        tracks.append(unidecode.unidecode(trackName))
      return tracks
  return None


def get_song_order(song, tracks):
  lower = unidecode.unidecode(song.decode('utf-8')).lower()
  for (i, track) in enumerate(tracks):
    if lower in track.lower():
      return i

  return -1


if __name__ == '__main__':
  siteDir = path.join(path.dirname(sys.argv[0]), 'site')

  src = sys.argv[1]
  dst = sys.argv[2]

  with open(path.join(siteDir, 'lyrics.html')) as f:
    lyricsLines = f.readlines()

  headerLines = find(lyricsLines, '<div id="header">')
  contentLines = find(lyricsLines, '<div id="content">')
  previousLine = find(lyricsLines, PREVIOUS_FILE)
  nextLine = find(lyricsLines, NEXT_FILE)

  links = []
  songs = sorted(listdir(src))

  # Play Music Client
  mc = Mobileclient()
  mc.oauth_login(Mobileclient.FROM_MAC_ADDRESS)

  tracks = get_playlist_tracks(mc, 'Spanish')

  sorted_songs = [None] * len(songs)

  for song in songs:
    order = get_song_order(song, tracks)
    sorted_songs[order] = song

  for (songNumber, song) in enumerate(sorted_songs):
    dir = path.join(src, song)

    with open(path.join(dir, "original.txt")) as f:
      originalLines = f.readlines()
    with open(path.join(dir, "translated.txt")) as f:
      translatedLines = f.readlines()

    if len(originalLines) != len(translatedLines):
      print 'Line mismatch. Aborting'
      exit(1)

    lines = copy.deepcopy(lyricsLines)

    lines.insert(headerLines, TITLE_FORMAT.format(originalLines[0].strip(), translatedLines[0].strip()))
    at = contentLines + 1  # Because we inserted a title line.
    maxLine = 0
    for (lineNumber, line) in enumerate(originalLines[1:]):
      line = line.strip()
      if len(line) > maxLine:
        maxLine = len(line)

      if line == '':
        lines.insert(at, EMPTY_LINE)
      else:
        translatedLine = translatedLines[lineNumber + 1].strip()
        if len(translatedLine) > maxLine:
          maxLine = len(translatedLine)
        lines.insert(at, LINE_FORMAT.format(line, translatedLine))
      at += 1

    htmlFilename = toHtmlFileName(song)
    links += LINK_FORMAT.format(htmlFilename, song)

    if songNumber == len(sorted_songs) - 1:
      del lines[nextLine]
    else:
      nextSong = sorted_songs[songNumber + 1]
      lines[nextLine] = lines[nextLine].replace(NEXT_NAME, nextSong).replace(NEXT_FILE, toHtmlFileName(nextSong))

    if songNumber == 0:
      del lines[previousLine]
    else:
      previousSong = sorted_songs[songNumber - 1]
      lines[previousLine] = lines[previousLine].replace(PREVIOUS_NAME, previousSong).replace(PREVIOUS_FILE,
                                                                                             toHtmlFileName(
                                                                                               previousSong))

    with open(path.join(dst, htmlFilename), 'w') as f:
      f.writelines(lines)

    for file in COPY_FILES:
      copyfile(path.join(siteDir, file), path.join(dst, file))

  with open(path.join(siteDir, 'index.html')) as f:
    indexLines = f.readlines()

  at = find(indexLines, '<body>')
  for link in links:
    indexLines.insert(at, link)
    at += 1

  with open(path.join(dst, 'index.html'), 'w') as f:
    f.writelines(indexLines)
