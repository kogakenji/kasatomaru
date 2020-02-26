from bs4 import BeautifulSoup
import lxml.html
import pathlib
import db
import datetime

def files_list(start, end):
    """Generate url list with given start and end of indexes"""
    resultlist = []
    for i in range(start, end):
        resultlist.append(f"page_{i}.html")
    return resultlist

def extract_main_pages():
    """Extracts content from main pages """
    pages = files_list(1, 49278)
    # There was a problematic file: 44663.html removed #&...
    print(len(pages))
    for page in pages:
        path = pathlib.Path.cwd().parent / "main_files" / page
        print(path)
        with open(str(path), encoding="ISO-8859-1") as p:
            soup = BeautifulSoup(p.read(), 'html.parser')
            # soup = BeautifulSoup(p.read(), 'lxml')

            # table = soup.find_all("table", bgcolor="#FFFFFF")
            # print(table)

            data = soup.find_all("tr", {'class': 'texto'})

            for i, d in enumerate(data):
                tds = data[i].find_all('td')

                ship = tds[0].a.contents[0].strip()
                link_family = "http://www.museubunkyo.org.br/ashiato/web2/" + tds[1].a.get("href")
                family_id_register = link_family[link_family.find("=") + 1:link_family.index("&")]
                leave_date = tds[1].a.contents[0].strip()
                leave_date = datetime.datetime.strptime(leave_date, '%m/%d/%Y').strftime('%d/%m/%y')
                arrive_date = tds[1].a.contents[2].strip()
                arrive_date = datetime.datetime.strptime(arrive_date, '%m/%d/%Y').strftime('%d/%m/%y')
                province = tds[2].a.contents[0].strip()
                destination = tds[3].a.contents[0].strip()
                surname = tds[4].a.contents[0][0:4].strip()
                name = tds[5].a.contents[0].strip()
                print(
                    f"Ship: {ship} - leave_date: {leave_date} - arrive_date: {arrive_date} - province: {province} - destination: {destination} - surname: {surname} - name: {name}")
                # print(f"link_family: {link_family} - idRegistro: {id_register}")
                db.insert_person(name, surname, province, ship, destination, leave_date, arrive_date, link_family,
                                 family_id_register)

def extract_family_content():
    """Extracts content from family pages"""
    pass

if __name__ == "__main__":
    # extract_main_pages()

