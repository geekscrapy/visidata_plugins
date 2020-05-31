__author__ = 'Geekscrapy'
__version__ = '1.0'
__description__ = '''
Allows the user to fix the position on the page where they would like the
cursor to "stick". Helps to provide context about surrounding rows when
near the top and bottom of the page.

Usage: import this .py into .visidatarc, open a sheet, scroll a few
lines down, press "w" and scroll again!

Idea birthed here: https://github.com/saulpw/visidata/issues/561
'''
from visidata import option, options, status, Sheet

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
