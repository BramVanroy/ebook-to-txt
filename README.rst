Installation
============

1. Clone this repository
2. Enter the directory you cloned it into
3. :code:`pipenv install`

Usage
=====


.. code-block:: bash

    usage: convert_ebook_to_txt.py [-h] [-f FILE] [-d DIRECTORY] [-s SUFFIX]
                                   [--skip-last]

    Convert eBooks to text files. The conversions are saved under the same name
    with a .txt extension.

    optional arguments:
      -h, --help            show this help message and exit
      -f FILE, --file FILE  File to convert. (default: None)
      -d DIRECTORY, --directory DIRECTORY
                            Directory to convert. All files in it with the given
                            suffix will be converted to text files. (default:
                            None)
      -s SUFFIX, --suffix SUFFIX
                            When 'directory' is specified, all files with this
                            suffix will be converted. (default: .epub)
      --skip-last           Skip the last document in a file. These can be 'Thank
                            you for purchasing' notes. (default: False)
