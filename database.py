# -*- coding: utf-8 -*-
"""
database.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

BatteryDataBase data structures.
author: Shu Huang (sh2009@cam.ac.uk)
"""

from chemdataextractor_batteries.chemdataextractor15 import Document
import json
import copy


class BatteryDataBase:

    def __init__(self, paper_root, save_root, filename):
        self.dic = None
        self.filename = filename
        self.paper_root = paper_root
        self.count = 0
        self.save_root = save_root

    def write_into_file(self):
        with open('{}/{}.json'.format(self.save_root, self.filename), 'a', encoding='utf-8') as json_file:
            json.dump(self.dic, json_file, ensure_ascii=False)
            json_file.write('\n')
        return

    def extract(self, file):
        """

        :param file: The parsing files (HTML/XML...)
        :return: Write the record into the documents
        """
        # try:
        f = open(file, 'rb')
        d = Document.from_file(f)
        print('parsing ' + file)
        rough = d.records.serialize()
        print(rough)
        data = []
        for dic in rough:
            if 'Compound' in dic:
                continue
            try:
                dic['metadata'] = d.metadata[0].serialize()
                if dic['metadata']['doi'] == "None":
                    pass
            except BaseException:
                pass
            self.count += 1
            if self.is_valid(dic):
                dic_list = self.distribute(dic)
                data += dic_list
        if len(data) <= 3:
            for i in data:
                i['warning'] = 1
        for new_dic in data:
            self.dic = new_dic
            self.write_into_file()
        print(str(self.count) + ' relations in total')
        print(file + ' is done')
        f.close()
        # except BaseException:
        #     pass

    def is_valid(self, dic):
        """
        Check if the data record is valid or not
        :param dic:
        :return:
        """
        if "BatteryVolumeCapacity" in dic:
            return False
        else:
            try:
                if 'names' in next(iter(dic.values()))['compound']['Compound']:
                    return True
            except BaseException:
                return False

    def distribute(self, dic):
        """
        Extract chemical names if a length of a list > 1

        :param dic: A dictionary returned by CDE
        :return: A list of dictionaries with valid records
        """
        # Create a key 'names' (list)
        name_length = next(iter(dic.values()))['compound']['Compound']['names']
        next(iter(dic.values()))['names'] = [name_length[0]]
        if len(name_length) > 1:
            for j in name_length[1:]:
                if j.lower() not in [x.lower()
                                     for x in next(iter(dic.values()))['names']]:
                    next(iter(dic.values()))['names'].append(j)

        # Update the key 'value' as a list of float
        next(iter(dic.values()))['value'] = json.loads(
            next(iter(dic.values()))['value'])

        # Distribute
        dic_lists = self.distribute_value_and_names(dic)

        return dic_lists

    def distribute_value_and_names(self, dic):
        """
        Distribute the value and names into a list of dictionaries

        :param dic: A single dictionary, with keys 'names' and 'value' as 2 lists
        :return: A list of dictionaries with single name and value
        """
        dic_list = []
        len_names = len(next(iter(dic.values()))['names'])
        len_values = len(next(iter(dic.values()))['value'])
        copydic = copy.deepcopy(dic)
        if len_names == 1 and len_values == 1:
            next(iter(copydic.values()))['value'] = next(
                iter(dic.values()))['value'][0]
            next(iter(copydic.values()))['names'] = next(
                iter(dic.values()))['names'][0]
            dic_list.append(copydic)
        elif len_names == 1 and len_values > 1:
            for j in range(len_values):
                next(iter(copydic.values()))['value'] = float(
                    next(iter(dic.values()))['value'][j])
                next(iter(copydic.values()))['names'] = next(
                    iter(dic.values()))['names'][0]
                dic_list.append(copydic)
        elif len_names > 1 and len_values == 1:
            for j in range(len_names):
                next(iter(copydic.values()))['value'] = float(
                    next(iter(dic.values()))['value'][0])
                next(iter(copydic.values()))['names'] = next(
                    iter(dic.values()))['names'][j]
                dic_list.append(copydic)
        elif len_names == len_values and len_names > 1:
            for j in range(len_names):
                next(iter(copydic.values()))['value'] = float(
                    next(iter(dic.values()))['value'][j])
                next(iter(copydic.values()))['names'] = next(
                    iter(dic.values()))['names'][j]
                dic_list.append(copydic)
        else:
            for j in range(len_names):
                for k in range(len_values):
                    next(iter(copydic.values()))['value'] = float(
                        next(iter(dic.values()))['value'][k])
                    next(
                        iter(
                            copydic.values()))['names'] = next(
                        iter(
                            dic.values()))['names'][j]
                    dic_list.append(copydic)
        return dic_list
