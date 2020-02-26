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
                      province text,
                      ship text,
                      destination text,
                      leave_date text,
                      arrive_date text,
                      link_family text,
                      id_family_register integer)""")
    conn.commit()


def insert_person(name, surname, province, ship, destination, leave_date, arrive_date, link, id_family_register):
    # Insert a row of data
    sql = """INSERT INTO person (name,
                              surname,
                              province,
                              ship,
                              destination,
                              leave_date,
                              arrive_date,
                              link_family,
                              id_family_register)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
          """

    cursor.execute(sql, (name, surname, province, ship, destination, leave_date, arrive_date, link, id_family_register))
    conn.commit()

def families():
    sql = """SELECT distinct(id_family_register), link_family
             FROM person
             group by id_family_register
             order by id_family_register asc
          """

    people = cursor.execute(sql)
    return list(people)


if __name__ == "__main__":
    # create_db()
    print(len(families()))
    # insert_person("Kenji", "Koga", "Brazil", "Hokkaido", "Kasatomaru", "10/10/1980", "localhost", 12342, "10/12/1980")