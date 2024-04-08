import sqlite3

def createTable():
    commands = ["""CREATE TABLE IF NOT EXISTS lots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT NOT NULL,
                    description TEXT NOT NULL,
                    img TEXT)""",
                """CREATE TABLE IF NOT EXISTS bids (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lot_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    price INTEGER NOT NULL)""",
                ]
    con = sqlite3.connect('server/db.db')
    cur = con.cursor()
    for command in commands:
        cur.execute(command)
    con.commit()
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



