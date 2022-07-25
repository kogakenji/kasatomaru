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

def create_db():
    create_person()
    create_person_jp()
    conn.commit()
    disconnect()

def create_person():
    # Create table
    try:
        # cursor.execute("""DROP TABLE person""")
        cursor.execute("""CREATE TABLE person(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        name text,
                        surname text,
                        name_kanji text,
                        surname_kanji text,
                        province text,
                        ship text,
                        destination text,
                        leave_date text,
                        arrive_date text,
                        link_family text,
                        farm text,
                        station text,
                        id_family_register integer)""")
    except Exception as exp:
        print(f"Error: {exp}")

def create_person_jp():
    # Create table
    try:
        # cursor.execute("""DROP TABLE person_jp""")
        cursor.execute("""CREATE TABLE person_jp(
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
    except Exception as exp:
        print(f"Error: {exp}")   


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


def insert_person_jp(name, surname, province, ship, destination, leave_date, arrive_date, link, id_family_register):
    # Insert a row of data
    sql = """INSERT INTO person_jp (name,
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


def insert_japanese_name_into_person():
    sql = """SELECT id, name, surname
                 FROM person_jp
              """
    kanji_names = cursor.execute(sql)
    list_names = list(kanji_names)
    for id, name_kanji, surname_kanji in list_names:
        print(f"id: {id}, name_kanji: {name_kanji}, surname_kanji: {surname_kanji}")
        sql2 = """UPDATE person SET name_kanji = ?,
                                surname_kanji = ?
                                WHERE id = ?
            """

        cursor.execute(sql2, (name_kanji, surname_kanji, id))
        conn.commit()


# Queries used by API
def get_family_by_surname(surname):
    sql = """SELECT name, surname, name_kanji, surname_kanji, province, ship, destination, leave_date, arrive_date, farm, station
            FROM person
            WHERE surname = ?
          """
    people = cursor.execute(sql, (surname.upper(),))
    r = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    return r


if __name__ == "__main__":
    # create_db()
    # insert_japanese_name_into_person()
    get_family_by_surname("KOGA")
