from bs4 import BeautifulSoup
import lxml.html
import pathlib

def files_list(start, end):
    """Generate url list with given start and end of indexes"""
    resultlist = []
    for i in range(start, end):
        resultlist.append(f"page_{i}.html")
    return resultlist



if __name__ == "__main__":
    # to_extract = files_list(1, 49276)
    pages = files_list(1, 5)
    print(pages)
    for page in pages:
        path = pathlib.Path.cwd().parent / "crawler" / page
        print(path)
        with open(str(path), encoding="ISO-8859-1") as p:
            # print(p.read())
            # soup = BeautifulSoup(p.read(), 'html.parser')
            soup = BeautifulSoup(p.read(), 'lxml')

            table = soup.find_all("table", bgcolor="#FFFFFF")

            data = soup.find_all("tr",{'class':'texto'})

            print(data)
            print(type(data))
            print(len(data))
            # for item in data:
            #     soup_tr = BeautifulSoup(item.text, "lxml")
            #     tds = soup.find_all("td")
            #     count = 0
            #     for td in tds:
            #         print(count, td.text)
            #         count += 1