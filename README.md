# batterydatabase

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](https://github.com/shuhuang/batterygui/blob/master/LICENSE)

Tools for auto-generating the battery materials database.

## Installation

Please first install the public ChemDataExtractor version (v1.3):
```
conda install -c chemdataextractor chemdataextractor
```

Download the necessary data files (machine learning models, dictionaries, etc.):
```
cde data download
```

Then install the dependency packages for the bespoke version for batteries (chemdataextractor_batteries v1.5):
```
pip install -r requirements.txt
```

## Usage

To extract raw data from text, you need to provide the root of the paper folder, output root to data record folder, start and end index of papers, and the file name to be saved.

For example, extract the first paper of `test/` and save to `save/` as `raw_data.json`:
```
python extract.py --input_dir test/ --output_dir save/ --start 0 --end 1 --save_name raw_data
```

After the raw data is extracted, it needs to be cleaned and converted into a standard format. We provide the data cleaning code in `dataclean.ipynb`. The final data format can be `.json`, `.csv` or `.db`.

## Citation
```
@article{huang2020database,
  title={A database of battery materials auto-generated using ChemDataExtractor},
  author={Huang, Shu and Cole, Jacqueline M},
  journal={Scientific Data},
  volume={7},
  number={1},
  pages={1--13},
  year={2020},
  publisher={Nature Publishing Group}
}
```
[![DOI](https://zenodo.org/badge/DOI/10.1038/s41597-020-00602-2.svg)](https://doi.org/10.1038/s41597-020-00602-2)
