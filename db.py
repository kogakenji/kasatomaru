"""
Database creation and functionality
"""
import sqlite3
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "kasatomaru.db")


def connect():
    try:
        conn = sqlite3.connect(db_path)
        print("Connection is established")
        return conn
    except Exception as exp:
        print(f"Error connecting to database {exp}")


conn = connect()
cursor = conn.cursor()

def create_db():
    # Create table
    cursor.execute("""CREATE TABLE person(
                      id integer PRIMARY KEY AUTOINCREMENT,
                      name text,
                      surname text,
                      destination text,
                      province text,
                      ship text,
                      leave_date text,
                      link_family text,
                      id_register integer,
                      arrive_date)""")
    conn.commit()


def insert_person(name, surname, destination, province, ship, leave_date, link, id_register, arrive_date):
    # Insert a row of data
    sql = """INSERT INTO person (name,
                              surname,
                              destination,
                              province,
                              ship,
                              leave_date,
                              link_family,
                              id_register,
                              arrive_date)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
          """

    cursor.execute(sql, (name, surname, destination, province, ship, leave_date, link, id_register, arrive_date))
    conn.commit()

if __name__ == "__main__":
    # create_db()
    # insert_person("Kenji", "Koga", "Brazil", "Hokkaido", "Kasatomaru", "10/10/1980", "localhost", 12342, "10/12/1980")