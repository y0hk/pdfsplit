#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' PDF split
    A3-sized material landscape orientation ->
    A4-sized material portrait orientation

Usage:
  pdfsplit.py [-h] <file>

Options:
  -h --help     Show this screen.
  --version     Show version.

'''

from docopt import docopt
import os, copy
from hashids import Hashids
from PyPDF2 import PdfFileReader, PdfFileWriter

def main():
    arg = docopt(__doc__)
    filepath = arg.pop('<file>')
    if(filepath is False):
        print(__doc__)
        return

    original_L = PdfFileReader(open(filepath, 'rb'))
    pagenum = original_L.getNumPages()
    outpdf = PdfFileWriter()
    for i in range(pagenum):
        page_L = original_L.getPage(i)
        page_R = copy.copy(page_L)
        page_L.mediaBox.lowerRight = (
            842,
            595,
        )
        page_L.rotateClockwise(270)
        outpdf.addPage(page_L)

        page_R.mediaBox.upperLeft = (
            0,
            595
        )
        page_R.rotateClockwise(270)
        outpdf.addPage(page_R)

    root, ext = os.path.splitext(filepath)
    id = Hashids(salt='Split PDF').encode(321)
    outfilepath = root + id + ext

    outputStream = open(outfilepath, 'wb')
    outpdf.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
   main()