#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from typing import Optional
from typing import Sequence


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    for filename in args.filenames:
        with open(filename, mode='rb') as file_processed:
            if 'wdb' in file_processed.read():
                print('Il y a un WDB jenny !!')
                return False

