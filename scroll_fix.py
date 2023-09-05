'''
Enables two functions:
1. scrolloff: determines the number of context lines you would like to see above and below the cursor. The following command scrolls the text so that (when possible) there are always at least five lines visible above the cursor, and five lines visible below the cursor
2. scrollfix: Lock the cursor to a particular row number in the view

Allows the user to fix the position on the page where they would like the
cursor to "stick". Helps to provide context about surrounding rows when
near the top and bottom of the page.

Usage: import this .py into .visidatarc, open a sheet, scroll a few
lines down, press "w" and scroll again!

NOTE:
    - scrollfix mode disables use off scroll-middle command
'''

__author__ = 'Geekscrapy'
__version__ = '1.2'

from visidata import option, Sheet, ALT


@Sheet.api
def checkCursor(sheet):
    checkCursor.__wrapped__(sheet)

    disp_scrolloff = sheet.options.disp_scrolloff
    if disp_scrolloff:
        if disp_scrolloff >= int(sheet.nScreenRows/2):
            if sheet.cursorRowIndex+1 > int(sheet.nScreenRows/2):
                sheet.topRowIndex = sheet.cursorRowIndex - int(sheet.nScreenRows/2)
        else:
            if sheet.cursorRowIndex-sheet.topRowIndex < disp_scrolloff:
                sheet.topRowIndex = max(0, sheet.cursorRowIndex-sheet.options.disp_scrolloff)

            if sheet.bottomRowIndex-sheet.cursorRowIndex < disp_scrolloff:
                sheet.bottomRowIndex = sheet.cursorRowIndex+disp_scrolloff

    if hasattr(sheet, 'disp_scrollfix') and sheet.disp_scrollfix > 0:
        cursorViewIndex = sheet.cursorRowIndex - sheet.topRowIndex
        if cursorViewIndex > sheet.disp_scrollfix:
            sheet.topRowIndex += abs(sheet.disp_scrollfix - cursorViewIndex)
        if cursorViewIndex < sheet.disp_scrollfix and sheet.topRowIndex > 0:
            sheet.topRowIndex -= abs(sheet.disp_scrollfix - cursorViewIndex)

option(name='disp_scrolloff', default=5, helpstr='context lines to display above/below cursor when scrolling')

Sheet.addCommand(ALT+'w', 'scrollfix-toggle', 'sheet.disp_scrollfix, _ = (-1, status("unlocked")) if hasattr(sheet, "disp_scrollfix") and sheet.disp_scrollfix>0 else (cursorRowIndex - topRowIndex, status("locked"))', helpstr='toggle scrollfix behaviour. lock cursor view to a static row number')
