import sqlite3

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("Sqllite "+sqlite3.version)
    except sqlite3.Error as e:
        print(e)
        conn.close()
        return 0
    return conn