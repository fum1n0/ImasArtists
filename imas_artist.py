# coding: utf-8

import os
from glob import glob
import numpy as np
import subprocess
import argparse
import shutil
import csv

from mutagen.flac import FLAC

parser = argparse.ArgumentParser(description='')
parser.add_argument('--idol_path', dest='idol_path',
                    default='./idol.csv', help='path of the idol csv')
parser.add_argument('--units_path', dest='units_path',
                    default='./units.csv', help='path of the units csv')
parser.add_argument('--flac_dir', dest='flac_dir',
                    default='./flac', help='path of the flac dir')
args = parser.parse_args()


def load_artistlist(artists_path):
    with open(artists_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        header = next(reader)
        idol_names = []
        va_names = []
        for row in reader:
            idol_names.append(row[0])
            va_names.append(row[1])

    artist_names = []
    for i in range(min(len(idol_names), len(va_names))):
        artist_names.append('{}(CV:{})'.format(idol_names[i], va_names[i]))
        idol_names[i].replace(' ', '')
        artist_names[i].replace(' ', '')

    return idol_names, artist_names


def load_unitslist(units_path):
    with open(units_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')
        header = next(reader)
        units_dict = {}
        for row in reader:
            units_dict.update({row[0]: row[1:]})
    return units_dict


def is_unit(unit_dict, artists):
    for key in unit_dict.keys():
        flag = True
        for unit_idol in unit_dict[key]:
            if not (unit_idol in artists):
                flag = False
        if flag:
            name = key + "["
            for unit_idol in unit_dict[key]:
                name = name + unit_idol + ", "
            name = name[:-2] + "]"
            return flag, name

    return False, ''


def load_flaclist(flac_dir):
    if not os.path.exists(flac_dir):
        print("Not Flac Directory")
        os.sys.exit()
    return glob('{}/*.flac'.format(flac_dir))


if __name__ == '__main__':

    idol_names, artist_names = load_artistlist(args.idol_path)
    unit_dict = load_unitslist(args.units_path)
    flac_paths = load_flaclist(args.flac_dir)

    for flac_path in flac_paths:
        artists = []
        audio = FLAC(flac_path)
        flac_artist = audio['artist'][0].replace(' ', '')

        for i in range(min(len(idol_names), len(artist_names))):
            if(idol_names[i] in flac_artist):
                artists.append(artist_names[i])

        if 0 < len(artists):
            name = ''
            for artist in artists:
                name = '{}, {}'.format(name, artist)
            name = name[2:]
            flag, unit_name = is_unit(unit_dict, name)
            if flag:
                name = unit_name

            audio['artist'] = name
            audio.save()
