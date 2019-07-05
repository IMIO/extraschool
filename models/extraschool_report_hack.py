# -*- coding: utf-8 -*-
##############################################################################
#
#    Extraschool
#    Copyright (C) 2008-2019
#    Jean-Michel Abé - Town of La Bruyère (<http://www.labruyere.be>)
#    Michael Michot & Michael Colicchia - Imio (<http://www.imio.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import pdb
from odoo.osv import osv
from pyPdf import PdfFileWriter, PdfFileReader
import tempfile
from contextlib import closing
import os
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

class extraschool_report_hack(osv.Model):
    _inherit = 'report'

#     def _merge_pdf(self, documents):
#         """Merge PDF files into one.
# 
#         :param documents: list of path of pdf files
#         :returns: path of the merged pdf
#         """
#         blankpdfstr = '''JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmoKPDwvTGVuZ3RoIDMgMCBSL0ZpbHRlci9GbGF0ZURl
# Y29kZT4+CnN0cmVhbQp4nDPQM1Qo5ypUMFAwALJMLU31jBQsTAz1LBSKUrnCtRTyuAIVAIcdB3IK
# ZW5kc3RyZWFtCmVuZG9iagoKMyAwIG9iago0MgplbmRvYmoKCjUgMCBvYmoKPDwKPj4KZW5kb2Jq
# Cgo2IDAgb2JqCjw8L0ZvbnQgNSAwIFIKL1Byb2NTZXRbL1BERi9UZXh0XQo+PgplbmRvYmoKCjEg
# MCBvYmoKPDwvVHlwZS9QYWdlL1BhcmVudCA0IDAgUi9SZXNvdXJjZXMgNiAwIFIvTWVkaWFCb3hb
# MCAwIDU5NSA4NDJdL0dyb3VwPDwvUy9UcmFuc3BhcmVuY3kvQ1MvRGV2aWNlUkdCL0kgdHJ1ZT4+
# L0NvbnRlbnRzIDIgMCBSPj4KZW5kb2JqCgo0IDAgb2JqCjw8L1R5cGUvUGFnZXMKL1Jlc291cmNl
# cyA2IDAgUgovTWVkaWFCb3hbIDAgMCA1OTUgODQyIF0KL0tpZHNbIDEgMCBSIF0KL0NvdW50IDE+
# PgplbmRvYmoKCjcgMCBvYmoKPDwvVHlwZS9DYXRhbG9nL1BhZ2VzIDQgMCBSCi9PcGVuQWN0aW9u
# WzEgMCBSIC9YWVogbnVsbCBudWxsIDBdCi9MYW5nKGZyLUZSKQo+PgplbmRvYmoKCjggMCBvYmoK
# PDwvQ3JlYXRvcjxGRUZGMDA1NzAwNzIwMDY5MDA3NDAwNjUwMDcyPgovUHJvZHVjZXI8RkVGRjAw
# NEMwMDY5MDA2MjAwNzIwMDY1MDA0RjAwNjYwMDY2MDA2OTAwNjMwMDY1MDAyMDAwMzMwMDJFMDAz
# NT4KL0NyZWF0aW9uRGF0ZShEOjIwMTIxMTAzMTQ0NzEwKzAxJzAwJyk+PgplbmRvYmoKCnhyZWYK
# MCA5CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDIyNiAwMDAwMCBuIAowMDAwMDAwMDE5IDAw
# MDAwIG4gCjAwMDAwMDAxMzIgMDAwMDAgbiAKMDAwMDAwMDM2OCAwMDAwMCBuIAowMDAwMDAwMTUx
# IDAwMDAwIG4gCjAwMDAwMDAxNzMgMDAwMDAgbiAKMDAwMDAwMDQ2NiAwMDAwMCBuIAowMDAwMDAw
# NTYyIDAwMDAwIG4gCnRyYWlsZXIKPDwvU2l6ZSA5L1Jvb3QgNyAwIFIKL0luZm8gOCAwIFIKL0lE
# IFsgPEYyMjBCNDlBNjRDOEEzRDY3QUFBQzNCODAwNkI5RkRDPgo8RjIyMEI0OUE2NEM4QTNENjdB
# QUFDM0I4MDA2QjlGREM+IF0KL0RvY0NoZWNrc3VtIC83NzUwQTAyMEVFNEUwQkU5NjVGMzBDNTND
# MkRGNUFGNgo+PgpzdGFydHhyZWYKNzM2CiUlRU9GCg=='''
#         writer = PdfFileWriter()
#         blank_page = PdfFileReader(StringIO.StringIO(blankpdfstr.decode("base64"))).pages[0]
#         streams = []  # We have to close the streams *after* PdfFilWriter's call to write()
#         for document in documents:
#             pdfreport = file(document, 'rb')
#             streams.append(pdfreport)
#             reader = PdfFileReader(pdfreport)
#             for page in range(0, reader.getNumPages()):
#                 writer.addPage(reader.getPage(page))
#             if reader.getNumPages() % 2: 
#                 writer.addPage(blank_page)
# 
#         merged_file_fd, merged_file_path = tempfile.mkstemp(suffix='.html', prefix='report.merged.tmp.')
#         with closing(os.fdopen(merged_file_fd, 'w')) as merged_file:
#             writer.write(merged_file)
# 
#         for stream in streams:
#             stream.close()
# 
#         return merged_file_path


    # def _build_wkhtmltopdf_args(self, paperformat, specific_paperformat_args=None):
        
    #     res = super(extraschool_report_hack,self)._build_wkhtmltopdf_args(paperformat, specific_paperformat_args)
    #     if '--dpi' in res:
    #         i = res.index('--dpi')
    #         del res[i] #delete --dpi key
    #         del res[i] #delete --dpi value
        
    #     if specific_paperformat_args and specific_paperformat_args.get('data-report-margin-bottom'):
    #         if "--margin-bottom" in res:
    #             res[res.index('--margin-bottom') + 1] =  str(specific_paperformat_args.get('data-report-margin-bottom')) + 'mm'
    #         else:
    #             res.extend(['--margin-bottom', str(specific_paperformat_args.get('data-report-margin-bottom')) + 'mm'])

    #     if specific_paperformat_args and specific_paperformat_args.get('data-report-margin-top'):
    #         if "--margin-top" in res:
    #             res[res.index('--margin-top') + 1] =  str(specific_paperformat_args.get('data-report-margin-top')) + 'mm'
    #         else:
    #             res.extend(['--margin-top', str(specific_paperformat_args.get('data-report-margin-top')) + 'mm'])
        
    #     if specific_paperformat_args and specific_paperformat_args.get('data-report-margin-right'):
    #         if "--margin-right" in res:
    #             res[res.index('--margin-right') + 1] = str(specific_paperformat_args.get('data-report-margin-right')) + 'mm'
    #         else:
    #             res.extend(['--margin-right', str(specific_paperformat_args.get('data-report-margin-right')) + 'mm'])
        
    #     if specific_paperformat_args and specific_paperformat_args.get('data-report-margin-left'):
    #         if "--margin-left" in res:
    #             res[res.index('--margin-left') + 1] = str(specific_paperformat_args.get('data-report-margin-left')) + 'mm'
    #         else:
    #             res.extend(['--margin-left', str(specific_paperformat_args.get('data-report-margin-left')) + 'mm'])
 
    #     return res
