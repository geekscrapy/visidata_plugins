# Rich copy tables to the clipboard for quick and easy paste into Word docs

import sys
from visidata import *

__author__ = 'Geekscrapy'
__version__ = '1.0'

@Sheet.api
def richCopy(sheet, rows):
  if not rows:
    fail('no %s selected' % sheet.rowtype)
  status('copying rows to clipboard')
  # Copy rows to the system clipboard
  # use tempfile to generate filename and delete file on context exit
  with tempfile.NamedTemporaryFile(suffix='.html') as temp:
    vd.sync(saveSheets(Path(temp.name), sheet))
    p = subprocess.Popen(
      ['textutil -stdin -strip -format html -convert rtf -stdout | pbcopy'],
      stdin=open(temp.name, 'r', encoding=options.encoding),
      stdout=subprocess.DEVNULL,
      close_fds=True,
      shell=True)
    p.communicate()
  status('copied %d %s to system clipboard' % (len(rows), sheet.rowtype))

if sys.platform == "darwin":
  Sheet.addCommand(None, 'richcopy-selected', 'richCopy(selectedRows)', 'yank (copy) current selected row(s) to system clipboard as rtf data')
else:
  status('richcopy currently only supports OSX (requires "textutil" and "pbcopy" commands)', priority=3)
