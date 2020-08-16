# -*- coding: utf-8 -*-
"""
extract.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract the raw battery data.

"""

from chemdataextractor_batteries.chemdataextractor import Document
import json
import copy


class BatteryDataBase():

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
        f = open(file, 'rb')
        d = Document.from_file(f)
        print('parsing ' + file)
        print(d.metadata)
        rough = d.records.serialize()
        data = []
        for dic in rough:
            try:
                dic['metadata'] = d.metadata[0].serialize()
                if dic['metadata']['doi'] == "None":
                    pass
            except BaseException:
                pass
            if "names" in dic and "capacities" in dic:
                data += dic
                dicts = dic["capacities"][0]
                name = dic["names"]
                if "specifier" in dicts:
                    save = {"BatteryCapacity": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"], "compound": {"Compound":{"names":name}} ,"value": json.loads(dicts["value"])[0], "units":dicts["units"], "specifier":dicts["specifier"]}, "metadata":dic['metadata']}
                else:
                    save = {"BatteryCapacity": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"], "compound": {"Compound":{"names":name}},
                                                "value": json.loads(dicts["value"])[0], "units": dicts["units"]}, "metadata": dic['metadata']}
                self.dic = save
                self.write_into_file()
                self.count += 1
            if "names" in dic and "voltages" in dic:
                data += dic
                dicts = dic["voltages"][0]
                name = dic["names"]
                if "specifier" in dicts:
                    save = {"BatteryVoltage": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                                "compound": {"Compound": {"names": name}},
                                                "value": json.loads(dicts["value"])[0], "units": dicts["units"],
                                                "specifier": dicts["specifier"]}, "metadata": dic['metadata']}
                else:
                    save = {"BatteryVoltage": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                                "compound": {"Compound": {"names": name}},
                                                "value": json.loads(dicts["value"])[0], "units": dicts["units"]},
                            "metadata": dic['metadata']}
                self.dic = save
                self.write_into_file()
                self.count += 1
            if "names" in dic and "coulombics" in dic:
                data += dic
                dicts = dic["coulombics"][0]
                name = dic["names"]
                if "specifier" in dicts:
                    save = {"BatteryCoulombic": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                               "compound": {"Compound": {"names": name}},
                                               "value": json.loads(dicts["value"])[0], "units": dicts["units"],
                                               "specifier": dicts["specifier"]}, "metadata": dic['metadata']}
                else:
                    save = {"BatteryCoulombic": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                               "compound": {"Compound": {"names": name}},
                                               "value": json.loads(dicts["value"])[0], "units": dicts["units"]},
                            "metadata": dic['metadata']}
                self.dic = save
                self.write_into_file()
                self.count += 1
            if "names" in dic and "energies" in dic:
                data += dic
                dicts = dic["energies"][0]
                name = dic["names"]
                if "specifier" in dicts:
                    save = {"BatteryEnergy": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                                 "compound": {"Compound": {"names": name}},
                                                 "value": json.loads(dicts["value"])[0], "units": dicts["units"],
                                                 "specifier": dicts["specifier"]}, "metadata": dic['metadata']}
                else:
                    save = {"BatteryEnergy": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                                 "compound": {"Compound": {"names": name}},
                                                 "value": json.loads(dicts["value"])[0], "units": dicts["units"]},
                            "metadata": dic['metadata']}
                self.dic = save
                self.write_into_file()
                self.count += 1
            if "names" in dic and "conductivities" in dic:
                data += dic
                dicts = dic["conductivities"][0]
                name = dic["names"]
                if "specifier" in dicts:
                    save = {"BatteryConductivity": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                              "compound": {"Compound": {"names": name}},
                                              "value": json.loads(dicts["value"])[0], "units": dicts["units"],
                                              "specifier": dicts["specifier"]}, "metadata": dic['metadata']}
                else:
                    save = {"BatteryConductivity": {"raw_value": dicts["raw_value"], "raw_units": dicts["raw_units"],
                                              "compound": {"Compound": {"names": name}},
                                              "value": json.loads(dicts["value"])[0], "units": dicts["units"]},
                            "metadata": dic['metadata']}
                self.dic = save
                self.write_into_file()
                self.count += 1
        if len(data) <= 3:
            for i in data:
                i['warning'] = 1
        print(str(self.count) + ' relations in total')
        print(file + ' is done')
        f.close()