from pathlib import Path

from bs4 import BeautifulSoup as bs
from ebooklib import epub, ITEM_DOCUMENT


def text_from_ebook(fin, *, skip_last=False):
    """ Get text from ebook. Optionally leave out the last document,
        which often is a note such as Thank you for purchasing this eBook'.

    :param fin: input file in eBook format (e.g. ePub)
    :param skip_last: skip the last document in the file
    :return: the extracted text
    """
    book = epub.read_epub(fin)
    docs = list(book.get_items_of_type(ITEM_DOCUMENT))
    n_docs = len(docs)
    texts = []
    for doc_idx, doc in enumerate(docs):
        if skip_last and doc_idx == n_docs-1:
            break
        soup = bs(doc.content, 'lxml')
        lines = list(filter(None, [l.strip() for l in soup.get_text().split('\n')]))

        if not lines:
            continue

        texts.append('\n'.join(lines))

    return '\n'.join(texts) + '\n'


def convert_directory(din, *, suffix='.epub', skip_last=False):
    """ Process all files with a given suffix in a given directory (non-recursively).
        Optionally leave out the last document.

    :param din: input directory whose files with a given suffix will be processed
    :param suffix: only files with this suffix will be processed
    :param skip_last: skip the last document in the file
    """
    for fin in Path(din).glob(f"*{suffix}"):
        convert_file(fin, skip_last=skip_last)


def convert_file(fin, *, skip_last=False):
    """ Get the extracted text from an ePub file and write it to an output file.
        The output file has the same name as the input file, but a .txt extension.

    :param fin: input file in eBook format (e.g. ePub)
    :param skip_last: skip the last document in the file
    """
    text = text_from_ebook(fin, skip_last=skip_last)
    with Path(fin).with_suffix('.txt').open('w', encoding='utf-8') as fhout:
        fhout.write(text)
    print(f"Successfully converted {fin}...")


if __name__ == '__main__':
    import argparse

    cparser = argparse.ArgumentParser(description='Convert eBooks to text files. The conversions are saved under '
                                                  ' the same name with a .txt extension.',
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    cparser.add_argument('-f', '--file', help='File to convert.')
    cparser.add_argument('-d', '--directory', help='Directory to convert. All files in it with the given suffix will be'
                                                   ' converted to text files.')
    cparser.add_argument('-s', '--suffix', default='.epub', help="When 'directory' is specified, all files with this"
                                                                 " suffix will be converted.")
    cparser.add_argument('--skip-last', action='store_true', default=False,
                         help="Skip the last document in a file. These can be 'Thank you for purchasing' notes.")

    cargs = cparser.parse_args()

    if cargs.file:
        convert_file(cargs.file, skip_last=cargs.skip_last)
    elif cargs.directory:
        convert_directory(cargs.directory, skip_last=cargs.skip_last, suffix=cargs.suffix)
    else:
        raise ValueError("'One of 'file' or 'directory' must be supplied.")
