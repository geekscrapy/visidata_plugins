from visidata import *

dt_map = {
    None:       'NULL',
    anytype:    'TEXT',
    date:       'DATETIME',
    str:        'TEXT',
    int:        'INTEGER',
    float:      'REAL',
    bytes:      'BLOB'
}

class SQLiteResultSheet(SequenceSheet):
    table_name = 'sheet'

    def iterload(self):
        self.columns = []
        import sqlite3

        with sqlite3.connect(':memory:') as conn:
            # create table
            new_cols = {}

            for col in Progress(self.source.visibleCols):
                ctype = dt_map.get(col.type, 'TEXT')
                new_cols[col.name] = ctype

            col_str = [' '.join(x) for x in new_cols.items()]
            conn.execute(f'CREATE TABLE {self.table_name}({ ", ".join(col_str) })')

            # insert values into sheet
            iQuery = f'INSERT OR IGNORE INTO {self.table_name} ({", ".join(new_cols)}) VALUES ({",".join(["?" for i in range(0,len(new_cols))])})'
            conn.executemany(
                iQuery,
                [row for row in Progress(self.get_rows(), gerund='inserting', total=len(self.source))]
            )

            # make headers
            cursor = conn.execute(self.query)
            yield tuple(map(lambda x: x[0], cursor.description))

            # convert headers to known col.types
            for c in self.columns:
                for ocol in filter(lambda oc: oc.name == c.name, self.source.columns):
                    c.type = ocol.type

            for r in Progress(cursor, gerund='selecting', total=cursor.rowcount):
                yield r

    def get_rows(self):
        for typedvals in self.source.iterdispvals(format=False):
            row = []
            for col, val in typedvals.items():
                if col.type in [None, int, float, str, bytes]:
                    val = val
                elif col.type == date:
                    val = val.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    val = str(val)
                row.append(val)
            yield tuple(row)

class SQLCompleter:

    # some of these are likely unusable
    sqlite_keywords = ['ABORT', 'ACTION', 'ADD', 'AFTER', 'ALL', 'ALTER', 'ALWAYS',
    'ANALYZE', 'AND', 'AS', 'ASC', 'ATTACH', 'AUTOINCREMENT', 'BEFORE', 'BEGIN',
    'BETWEEN', 'BY', 'CASCADE', 'CASE', 'CAST', 'CHECK', 'COLLATE', 'COLUMN',
    'COMMIT', 'CONFLICT', 'CONSTRAINT', 'CREATE', 'CROSS', 'CURRENT', 'CURRENT_DATE',
    'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'DATABASE', 'DEFAULT', 'DEFERRABLE', 'DEFERRED',
    'DELETE', 'DESC', 'DETACH', 'DISTINCT', 'DO', 'DROP', 'EACH', 'ELSE', 'END',
    'ESCAPE', 'EXCEPT', 'EXCLUDE', 'EXCLUSIVE', 'EXISTS', 'EXPLAIN', 'FAIL', 'FILTER',
    'FIRST', 'FOLLOWING', 'FOR', 'FOREIGN', 'FROM', 'FULL', 'GENERATED', 'GLOB',
    'GROUP', 'GROUPS', 'HAVING', 'IF', 'IGNORE', 'IMMEDIATE', 'IN', 'INDEX', 'INDEXED',
    'INITIALLY', 'INNER', 'INSERT', 'INSTEAD', 'INTERSECT', 'INTO', 'IS', 'ISNULL',
    'JOIN', 'KEY', 'LAST', 'LEFT', 'LIKE', 'LIMIT', 'MATCH', 'NATURAL', 'NO', 'NOT',
    'NOTHING', 'NOTNULL', 'NULL', 'NULLS', 'OF', 'OFFSET', 'ON', 'OR', 'ORDER',
    'OTHERS', 'OUTER', 'OVER', 'PARTITION', 'PLAN', 'PRAGMA', 'PRECEDING', 'PRIMARY',
    'QUERY', 'RAISE', 'RANGE', 'RECURSIVE', 'REFERENCES', 'REGEXP', 'REINDEX',
    'RELEASE', 'RENAME', 'REPLACE', 'RESTRICT', 'RIGHT', 'ROLLBACK', 'ROW', 'ROWS',
    'SAVEPOINT', 'SELECT', 'SET', 'TABLE', 'TEMP', 'TEMPORARY', 'THEN', 'TIES', 'TO',
    'TRANSACTION', 'TRIGGER', 'UNBOUNDED', 'UNION', 'UNIQUE', 'UPDATE', 'USING',
    'VACUUM', 'VALUES', 'VIEW', 'VIRTUAL', 'WHEN', 'WHERE', 'WINDOW', 'WITH', 'WITHOUT',
    '*', 'DATETIME', 'DATETIME(timestamp, "unixepoch")', SQLiteResultSheet.table_name]

    def __init__(self, sheet=None, extras=[]):
        self.sheet = sheet
        self.extras = extras
    def __call__(self, val, state):
        i = len(val)-1
        while val[i:].isidentifier() and i >= 0:
            i -= 1

        if i < 0:
            base = ''
            partial = val
        elif val[i] == '.':  # no completion of attributes
            return None
        else:
            base = val[:i+1]
            partial = val[i+1:]

        varnames = []
        varnames.extend(sorted((base+col.name) for col in self.sheet.columns if col.name.startswith(partial.upper()) or col.name.startswith(partial.lower())))
        varnames.extend(sorted( (base+kw) for kw in self.sqlite_keywords if kw.startswith(partial.upper()) ))
        varnames.extend(sorted( (base+ex) for ex in self.extras if ex.startswith(partial.upper()) or ex.startswith(partial.lower()) ))
        return varnames[state%len(varnames)]


@BaseSheet.command('z.', 'sqlite-query', 'perform sqlite query over sheet')
def sqlite_query(sheet):
    import sqlite3

    query = f'SELECT * FROM {SQLiteResultSheet.table_name} ;'
    prompt='sqlite query: '
    while True:
        query = vd.input(
            prompt=prompt,
            completer=SQLCompleter(sheet, extras=[SQLiteResultSheet.table_name]),
            type='sqlite',
            value=query
        )

        if not sqlite3.complete_statement(query):
            prompt = 'check syntax: '
            query = query
        else:
            break

    name = f'{sheet.name}-sql-{clean_name(query.replace("*", "x"))}'
    vs = SQLiteResultSheet(name, source=sheet, query=query)
    vd.push(vs)


# Over multiple sheets?!
# Map rowid(row) > sqlite rowid, can be used to group select
