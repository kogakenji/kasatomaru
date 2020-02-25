from bs4 import BeautifulSoup
import lxml.html
import pathlib
import db

def files_list(start, end):
    """Generate url list with given start and end of indexes"""
    resultlist = []
    for i in range(start, end):
        resultlist.append(f"page_{i}.html")
    return resultlist




if __name__ == "__main__":
    # to_extract = files_list(1, 49276)
    pages = files_list(1, 49276)
    print(len(pages))
    for page in pages:
        path = pathlib.Path.cwd().parent / "crawler" / page
        print(path)
        with open(str(path), encoding="ISO-8859-1") as p:
            # print(p.read())
            soup = BeautifulSoup(p.read(), 'html.parser')
            # soup = BeautifulSoup(p.read(), 'lxml')

            # table = soup.find_all("table", bgcolor="#FFFFFF")
            # print(table)

            data = soup.find_all("tr",{'class':'texto'})

            for i, d in enumerate(data):
                tds = data[i].find_all('td')

                ship = tds[0].a.contents[0]
                leave_date = tds[1].a.contents[0]
                link_family = "http://www.museubunkyo.org.br/ashiato/web2/"+tds[1].a.get("href")
                id_register = link_family[link_family.find("=")+1:link_family.index("&")]
                arrive_date = tds[1].a.contents[2]
                province = tds[2].a.contents[0]
                destination = tds[3].a.contents[0]
                surname = tds[4].a.contents[0]
                name = tds[5].a.contents[0]
                # print(f"Ship: {ship} - leave_date: {leave_date} - arrive_date: {arrive_date} - province: {province} - destination: {destination} - surname: {surname} - name: {name}")
                print(f"link_family: {link_family} - idRegistro: {id_register}")
                db.insert_person(name, surname, destination, province, ship, leave_date, link_family, id_register, arrive_date)
        break
