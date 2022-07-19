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
    # pages = files_list(5884, 5885)
    print(f"total pages: {len(pages)}")
    for page in pages:
        path = None
        if language == PORTUGUESE:
            path = pathlib.Path.cwd().parent / "files" / "pt"/ page
        elif language == JAPANESE:
            path = pathlib.Path.cwd().parent / "files" / "jp"/ page
        
        with open(str(path), encoding="ISO-8859-1") as p:
            # soup = BeautifulSoup(p.read(), 'html.parser')
            print(f"Processing file: {path}")
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
                try:
                    # tds_name = tds[7]
                    # print(f"surname: {surname} - tds_name: {tds_name}")
                    name = tds[7].a.contents[0].strip()
                except Exception as exp:
                    print(exp)
                try:
                    # print(
                    #     f"Ship: {ship} - leave_date: {leave_date} - arrive_date: {arrive_date} - province: {province} - destination: {destination} - surname: {surname} - name: {name}")
                    # print(f"link_family: {link_family} - idRegistro: {family_id_register}")
                    if language == PORTUGUESE:
                        db.insert_person(name, surname, province, ship, destination, leave_date, arrive_date, link_family,
                                        family_id_register)
                    elif language == JAPANESE:
                        db.insert_person_jp(name, surname, province, ship, destination, leave_date, arrive_date, link_family,
                                        family_id_register)
                except Exception as exp:
                    print(exp)
                    pass


def get_family_content(id_family_register):
    """
    Gets the family content of one family register
    """
    path = pathlib.Path.cwd().parent / "files" / "family"/ f"page_{id_family_register}.html" 

    with open(str(path), encoding="UTF-8") as p:
        soup = BeautifulSoup(p.read(), "lxml")
        # print("=================fazenda================")
        td = soup.find_all("div", class_='col-xs-4')
        td_farm = td[4].find_all("label", class_='textSubTitle')
        farm = td_farm[0].get_text()
        
        td_station = td[6].find_all("label", class_='textSubTitle')
        station = td_station[0].get_text()
        
        print(f"id_family_register: {id_family_register}, farm: {farm}, station: {station}")

        lock.acquire(True)
        try:
            # print(f"person: {p}")
            db.update_person_with_family_info(farm, station, id_family_register)
        except Exception as err:
            print(err)
            pass
        lock.release()


def extract_family_content():
    """Extracts content from family pages"""
    families = db.person_info()
    print(f"TOTAL SIZE: {len(families)}")
    for page in families:
        get_family_content(page[0])


if __name__ == "__main__":
    # extract_main_pages(PORTUGUESE)
    # extract_main_pages(JAPANESE)
     extract_family_content()

