import requests
from bs4 import BeautifulSoup
import lxml.html



URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Provincia=999&Navio=999&AnoChegada=999&Idioma=P"

def get_URL():
    r = requests.get(URL)
    # print(r.content)
    # soup = BeautifulSoup(r.content, 'html.parser')
    soup = BeautifulSoup(r.content, 'lxml')

    # table = soup.find_all("table", bgcolor="#FFFFFF")
    
    data = soup.find_all("tr",{'class':'texto'})

    print(data)
    print(type(data))
    print(len(data))
    for item in data:
        soup_tr = BeautifulSoup(item.text, "lxml")
        tds = soup.find_all("td")
        count = 0
        for td in tds:
            print(count, td.text)
            count += 1


if __name__ == "__main__":
    get_URL()