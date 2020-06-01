"""
Database creation and functionality
"""
import sqlite3
import os.path


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "kasatomaru.db")


def connect():
    try:

        conn = sqlite3.connect(db_path, check_same_thread = False)
        print("Connection is established")
        return conn
    except Exception as exp:
        print(f"Error connecting to database {exp}")

def disconnect():
    cursor.close()
    conn.close()

conn = connect()
cursor = conn.cursor()

def create_person():
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

def create_family():
    # Create table
    cursor.execute("""CREATE TABLE family(
                      id integer PRIMARY KEY,
                      FOREIGN KEY(id) REFERENCES person(id_family_register)  
                      name text,
                      surname text,
                      province text,
                      ship text,
                      destination text,
                      leave_date text,
                      arrive_date text,
                      link_family text,
                      id_family_register integer)""")


def insert_person(name, surname, province, ship, destination, leave_date, arrive_date, link, id_family_register):
    # Insert a row of data
    sql = """INSERT INTO jp_person (japanese_name,
                              japanese_surname,
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
    sql = """SELECT distinct(id_family_register) as id_family, link_family
             FROM person
             group by id_family_register
             order by id_family_register asc
          """

    people = cursor.execute(sql)
    return list(people)

def person_info():
    sql = """SELECT distinct(id_family_register)
                 FROM jp_person
                 WHERE farm is null and id_family_register > 10000
                 order by id_family_register
              """
    people = cursor.execute(sql)
    return list(people)

def update_family(name, surname, japanese_name, japanese_surname, ship, destination, leave_date, arrival_date, farm, station):
    # Insert a row of data
    sql = """UPDATE person 
             SET farm = ?,
                 station = ?,
                 japanese_name = ?,
                 japanese_surname =?
             WHERE name = ?
             AND surname = ?
             AND ship = ?
             AND destination = ?
             AND leave_date = ?
             AND arrive_date = ?
            """
    cursor.execute(sql, (farm, station, japanese_name, japanese_surname, name, surname, ship, destination, leave_date, arrival_date))
    conn.commit()

def update_jp_family(name, surname, japanese_name, japanese_surname, ship, destination, leave_date, arrival_date, farm, station):
    # Insert a row of data
    sql = """UPDATE jp_person 
             SET farm = ?,
                 station = ?,
                 name = ?,
                 surname = ?
             WHERE japanese_name = ?
             AND japanese_surname = ?
             AND ship = ?
             AND destination = ?
             AND leave_date = ?
             AND arrive_date = ?
            """
    cursor.execute(sql, (farm, station, name, surname, japanese_name, japanese_surname, ship, destination, leave_date, arrival_date))
    conn.commit()

if __name__ == "__main__":
    # create_db()
    print(len(families()))
    # insert_person("Kenji", "Koga", "Brazil", "Hokkaido", "Kasatomaru", "10/10/1980", "localhost", 12342, "10/12/1980")