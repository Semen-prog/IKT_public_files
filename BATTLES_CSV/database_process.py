import sqlite3, csv
from imutils import paths

def get_connection(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return conn, cur

def close_connection(conn):
    conn.commit()

def create_database():
    conn, cur = get_connection('battles.db')
    list_files = list(paths.list_files("csvs"))

    for path in list_files:
        name = path[5:-4]
        ask = "CREATE TABLE IF NOT EXISTS " + name + "(\n"
        with open('csvs/' + name + '.csv') as f:
            reader = list(csv.reader(f))
        for j in range(len(reader[0])):
            tp = "None"
            f1, f2 = True, True
            for i in range(1, len(reader)):
                if reader[i][j] == '':
                    reader[i][j] = 'NULL'
                    continue
                try:
                    reader[i][j] = int(reader[i][j])
                except:
                    f1 = False
                    try:
                        reader[i][j] = float(reader[i][j])
                    except:
                        f2 = False
            if f1:
                tp = "INT"
            elif f2:
                tp = "REAL"
            else:
                tp = "TEXT"
            ask += reader[0][j] + ' ' + tp
            if j == len(reader[0]) - 1:
                ask += ");"
            else:
                ask += ",\n"
        cur.execute(ask)
        for k in range(1, len(reader)):
            row = reader[k]
            ask = "INSERT INTO " + name + " VALUES("
            s = '?' * len(row)
            s = ', '.join(s)
            ask = ask + s + ");"
            cur.execute(ask, tuple(row))

    conn.commit()