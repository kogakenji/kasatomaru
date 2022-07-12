from bs4 import BeautifulSoup
import lxml.html
import pathlib
import db
import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

# Define the lock globally
lock = threading.Lock()
PORTUGUESE = "p"
JAPANESE = "j"
PORTUGUESE_PATH = "../files/pt"
JAPANESE_PATH = "../files/jp"
TOTAL_PAGES = 24566

def files_list(start, end):
    """Generate url list with given start and end of indexes"""
    resultlist = []
    for i in range(start, end):
        resultlist.append(f"page_{i}.html")
    return resultlist

def extract_main_pages(language):
    """Extracts content from main pages """
    pages = files_list(1, TOTAL_PAGES)
    print(f"total pages: {len(pages)}")
    for page in pages:
        path = None
        if language == PORTUGUESE:
            path = pathlib.Path.cwd().parent / "files" / "pt"/ page
        elif language = JAPANESE:
            path = pathlib.Path.cwd().parent / "files" / "jp"/ page
        
        with open(str(path), encoding="ISO-8859-1") as p:
            # soup = BeautifulSoup(p.read(), 'html.parser')
            soup = BeautifulSoup(p.read(), 'lxml')

            table = soup.find_all("div", class_='divrow')
            data = table[0].find_all("div", class_='divcol')
            for i, d in enumerate(table):
                tds = table[i].find_all("div", class_="divcol")

                ship = tds[0].a.contents[0].strip()
                link_family = "http://imigrantes.ubik.com.br" + tds[1].a.get("href")
                
                family_id_register = link_family[link_family.find('=')+1:]
                leave_date = tds[1].a.contents[0].strip()
                leave_date = datetime.datetime.strptime(leave_date, '%d/%m/%Y').strftime('%d/%m/%y')
                
                arrive_date = tds[2].a.contents[0].strip()
                arrive_date = datetime.datetime.strptime(arrive_date, '%d/%m/%Y').strftime('%d/%m/%y')
                
                province = tds[4].a.contents[0].strip()
                
                destination = tds[5].a.contents[0].strip()
                
                surname = tds[6].a.contents[0].strip()
                
                name = tds[7].a.contents[0].strip()
                try:
                    print(
                        f"Ship: {ship} - leave_date: {leave_date} - arrive_date: {arrive_date} - province: {province} - destination: {destination} - surname: {surname} - name: {name}")
                    # print(f"link_family: {link_family} - idRegistro: {family_id_register}")
                    db.insert_person(name, surname, province, ship, destination, leave_date, arrive_date, link_family,
                                    family_id_register)
                except Exception as exp:
                    print(exp)
                    pass

# def extract_jp_pages():
#     """Extracts content from main pages """
#     pages = files_list(1, 24566)
#     # There was a problematic file: 44663.html removed #&...
#     print(len(pages))
#     for page in pages:
#         path = pathlib.Path.cwd().parent / "files" / "jp" /page
#         print(path)
#         with open(str(path), encoding="ISO-8859-1") as p:
#             soup = BeautifulSoup(p.read(), 'html.parser')
#             # soup = BeautifulSoup(p.read(), 'lxml')

#             # table = soup.find_all("table", bgcolor="#FFFFFF")
#             # print(table)

#             data = soup.find_all("tr", {'class': 'texto'})

#             for i, d in enumerate(data):
#                 tds = data[i].find_all('td')

#                 ship = tds[0].a.contents[0].strip()
#                 link_family = "http://www.museubunkyo.org.br/ashiato/web2/" + tds[1].a.get("href")
#                 family_id_register = link_family[link_family.find("=") + 1:link_family.index("&")]
#                 leave_date = tds[1].a.contents[0].strip()
#                 leave_date = datetime.datetime.strptime(leave_date, '%m/%d/%Y').strftime('%d/%m/%y')
#                 arrive_date = tds[1].a.contents[2].strip()
#                 arrive_date = datetime.datetime.strptime(arrive_date, '%m/%d/%Y').strftime('%d/%m/%y')
#                 province = tds[2].a.contents[0].strip()
#                 destination = tds[3].a.contents[0].strip()
#                 surname = tds[4].a.contents[0][0:4].strip()
#                 name = tds[5].a.contents[0].strip()
#                 try:
#                     print(
#                         f"Ship: {ship} - leave_date: {leave_date} - arrive_date: {arrive_date} - province: {province} - destination: {destination} - surname: {surname} - name: {name}")
#                     # print(f"link_family: {link_family} - idRegistro: {id_register}")
#                     db.insert_person(name, surname, province, ship, destination, leave_date, arrive_date, link_family,
#                                      family_id_register)
#                 except Exception as exp:
#                     print(exp)
#                     pass

def has_class_but_no_id(tag):
    tag.has_attr('class') and tag.attrs()
    tag.contents
    return

class Ship():
    def __init__(self, name, leave_date, arrival_date, destination, farm, station):
        self.name = name
        self.leave_date = leave_date
        self.arrival_date = arrival_date
        self.destination = destination
        self.farm = farm
        self.station = station
    def __str__(self):
        return f"[SHIP_INFO]: Name:{self.name} LeaveDate:{self.leave_date} Arrival_date:{self.arrival_date} Destination:{self.destination} Farm:{self.farm} Station:{self.station}"

class Person():
    def __init__(self, name, surname, name_kanji, surname_kanji, ship):
        self.name = name
        self.surname = surname
        self.name_kanji = name_kanji
        self.surname_kanji = surname_kanji
        self.ship = ship
    def __str__(self):
        return f"[PERSON_INFO] Name:{self.name} Surname:{self.surname} NameKanji:{self.name_kanji} SurnameKanji:{self.surname_kanji} \n \t {self.ship}"

def get_family_content(id_family_register):
    # id, name, surname, id_family_register, link_family = family
    path = pathlib.Path.cwd().parent / "families_files" / "families" / f"page_{id_family_register[0]}.html"
    print(f"caminho do arquivo: {path}")

    with open(str(path), encoding="ISO-8859-1") as p:
        soup = BeautifulSoup(p.read(), "html.parser")
        # print(soup)
        # print("=================fazenda================")
        td = soup.find_all("span", {'class': 'titulo'})
        for titulo in td:
            if titulo.get_text() == "Navio:":
                ship = titulo.parent.get_text().split(': ')[1]
            if titulo.get_text() == "Destino:":
                destination = titulo.parent.get_text().split(': ')[1]
            if titulo.get_text() == "Partida:":
                leave_date = titulo.parent.get_text().split(': ')[1]
                leave_date = datetime.datetime.strptime(leave_date, '%m/%d/%Y').strftime('%d/%m/%y')
            if titulo.get_text() == "Chegada:":
                arrival_date = titulo.parent.get_text().split(': ')[1]
                arrival_date = datetime.datetime.strptime(arrival_date, '%m/%d/%Y').strftime('%d/%m/%y')
            if titulo.get_text() == "Fazenda:":
                farm = titulo.parent.get_text().split(': ')[1]
            if titulo.get_text() == "Estação:":
                station = titulo.parent.get_text().split(': ')[1]
        ship_info = Ship(ship, leave_date, arrival_date, destination, farm, station)
        # print("===================pessoas=====================")
        data = soup.find_all("tr", {'class': 'texto'})
        for d in data:
            record = d.find_all("td")
            list = [name.get_text() for name in record]
            p = Person(list[1], list[0], list[3], list[2], ship_info)

            lock.acquire(True)
            try:
                db.update_jp_family(p.name, p.surname, p.name_kanji, p.surname_kanji, p.ship.name, p.ship.destination,
                                 p.ship.leave_date, p.ship.arrival_date, p.ship.farm, p.ship.station)
            except Exception as err:
                print(err)
                pass
            lock.release()



def extract_family_content():
    """Extracts content from family pages"""
    families = db.person_info()
    print(f"TOTAL SIZE: {len(families)}")

    with ThreadPoolExecutor(max_workers=3) as executor:
        # executor.map(get_family_content, path)
        executor.map(get_family_content, families)


if __name__ == "__main__":
    extract_main_pages()
    #  extract_family_content()
    # extract_jp_pages()

