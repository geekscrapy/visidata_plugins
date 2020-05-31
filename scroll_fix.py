__author__ = 'Geekscrapy'
__version__ = '1.0'
# https://github.com/saulpw/visidata/issues/561

from visidata import *

option(name='scroll_fix_enabled', default=False, helpstr='toggle scroll fix')

@Sheet.api
def toggle_scroll_fix(sheet):

    # Disable scroll fix
    if options.scroll_fix_enabled:
        options.scroll_fix_enabled = False; status('scroll fix disabled')

        Sheet.addCommand(None, 'go-down',  'cursorDown(+1)', 'go down')
        Sheet.addCommand(None, 'go-up',    'cursorDown(-1)', 'go up')


    # Enable scrollfix
    else:
        options.scroll_fix_enabled = True; status('scroll fix enabled')

        Sheet.addCommand(None, 'go-up', 'sheet.topRowIndex -= 1; sheet.cursorRowIndex -= 1', 'move cursor up with a fixed position')
        Sheet.addCommand(None, 'go-down', 'sheet.topRowIndex = sheet.nRows - sheet.nScreenRows if sheet.topRowIndex + sheet.nScreenRows >= sheet.nRows else sheet.topRowIndex + 1; sheet.cursorRowIndex += 1', 'move cursor down with a fixed position')

Sheet.addCommand('w', 'scroll-fix-toggle', 'toggle_scroll_fix()', helpstr='toggle scroll fix behaviour')
