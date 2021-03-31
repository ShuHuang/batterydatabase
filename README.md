# batterydatabase

Tools for auto-generating battery material databases.

**Installation**

Please first install the public ChemDataExtractor version:
```
conda install -c chemdataextractor chemdataextractor
```

Then install the dependency packages:
```
pip install -r requirements.txt
```

**Usage**

To extract the raw data from articles, you need to provide the root of article folder, root to save the data records, starting and ending index of articles, and the file name.

For example, a command could be like this:

```
python extract.py '\test' '\save\' 0 1 'raw_data'
```

After the raw data is extracted, it needs to be cleaned and converted into a standard format. We've provided the data cleaning code in Jupyter Notebook dataclean.ipynb. The new version could be obtained after running through it.

Please refer to the source code for details.
