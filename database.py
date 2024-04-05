import sqlite3

def createTable():
    command = """CREATE TABLE IF NOT EXISTS lots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT NOT NULL,
                    description TEXT NOT NULL,
                    img TEXT)"""
    con = sqlite3.connect('mysite/db.db')
    cur = con.cursor()
    cur.execute(command)
    con.close()


def query(type,command,table='lots'):
    con = sqlite3.connect('server/db.db')
    cur = con.cursor()
    cur.execute(command)
    if type=='get':
        response = cur.fetchall()
    if type=='set':
        con.commit()
        cur.execute(f"SELECT * FROM {table} WHERE id={cur.lastrowid}")
        response = cur.fetchall()
    con.close()
    return response



