# -*- coding: utf-8 -*-

from database import BatteryDataBase
import os
import sys
import re


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
    paper_root = r'test/'
    save_root = r'save/'
    filename = 'test'
    create_db(paper_root, save_root, start=0, end=9, filename=filename)
    sys.exit()
