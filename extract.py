# -*- coding: utf-8 -*-
"""
extract.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract the raw battery data.

"""

from database import BatteryDataBase
import os
import sys
import re
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_dir", default=None, type=str,
                        help="The input data dir containing .html/.xml files.")
    parser.add_argument("--output_dir", default=None, type=str,
                        help="The output dir for json files of extracted data.")
    parser.add_argument("--start", type=int, default=0,
                        help='Start index in the input paper folder')
    parser.add_argument("--end", type=int, default=1,
                        help='End index in the input paper folder')
    parser.add_argument("--save_name", default='raw_data', type=str,
                        help="The save name of the json file.")
    args = parser.parse_args()

    return args


def sorted_aphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def paper_list(root):
    papers = []
    for d in sorted_aphanumeric(os.listdir(root)):
        if os.path.isdir(root + '/' + d):
            sub_papers = paper_list(root + '/' + d)
            for sp in sub_papers:
                papers.append(sp)
        elif os.path.isfile(root + '/' + d) and (d.endswith('.html') or d.endswith('.xml')):
            papers.append(root + '/' + d)
    return sorted_aphanumeric(papers)


def create_db(paper_root, save_root, start=0, end=None, filename='test'):
    # set up the database
    mdb = BatteryDataBase(
        paper_root=paper_root,
        save_root=save_root,
        filename=filename)
    paper_l = paper_list(paper_root)[int(start):int(end)]

    for file_n in paper_l:
        mdb.extract(file_n)
    return


if __name__ == '__main__':
    args = parse_arguments()
    
    if args.input_dir is None:
        raise ValueError('--input_dir must be provided via arguments')
    if args.output_dir is None:
        raise ValueError('--output_dir must be provided via arguments')

    # paper_root = r'test/'
    # save_root = r'save/'
    # filename = 'test'
    create_db(args.input_dir, args.output_dir, args.start, args.end, args.save_name)
    sys.exit()
