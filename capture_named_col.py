__version__ = '0.9' # Works for me :)
__author__ = 'Geekscrapy'

from visidata import *

def makeNamedRegexMatcher(grp_name, regex, origcol):
    def _regexMatcher(row):
        m = regex.search(origcol.getDisplayValue(row))
        if m:
            return m.group(grp_name)
    return _regexMatcher

@asyncthread
def addNamedRegexColumns(vs, colIndex, origcol, regexstr):
    regexstr or vd.fail('regex required')

    regex = re.compile(regexstr, vs.regex_flags())

    ncols = 0
    for grp_name in list(regex.groupindex):
        func = makeNamedRegexMatcher(grp_name, regex, origcol)
        c = Column(grp_name,
            getter=lambda col,row,func=func: func(row),
            origCol=origcol
        )
        vs.addColumn(c, index=colIndex+ncols+1)
        ncols += 1

Sheet.addCommand('z:', 'capture-named-col', 'addNamedRegexColumns(sheet, cursorColIndex, cursorCol, input("match named regex: ", type="regex-capture"))', 'add new columns from named capture groups of regex i.e. (?<name>.*?)\\s')
