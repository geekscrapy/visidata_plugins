# visidata plugins
- richcopy.py - Yank selected rows to the clipboard in richtext format for easy paste into Word etc. Only designed to work on OSX. If you need another OS, file an issue :)
- scroll_fix.py - Ability to keep the cursor in the same place (visually) when scrolling. Helps to provide context about surrounding rows when near the top and bottom of the page
- capture_named_col.py - Provides the ability to extract regex from a column to create new columns with names from the regex capture groups
- sql_selector.py - run sql queries against your "sheet". The sheets' table is named "sheet" in the SQL queries
- logging.py - allows visidata status(), warning(), debug() etc. to be logged to a file. Timestamps are always placed on the logs sent to the file unless the option format is modified (`options.log_*`). Log is saved to `vd.log` by default
