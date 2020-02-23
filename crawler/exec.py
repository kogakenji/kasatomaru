import requests
from bs4 import BeautifulSoup
import lxml.html
import threading
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures

URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Provincia=999&Navio=999&AnoChegada=999&Idioma=P"
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=2&PAG=T
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=1&PAG=F
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=2&PAG=F
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=3&PAG=F
FINAL_URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=49276&PAG=F"
INITIAL_URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Provincia=999&Busca=&Idioma=P&PAGATUAL="


def generate_urls(start, end):
    resultlist = []
    for i in range(start, end):
        resultlist.append(INITIAL_URL+str(i))
    return resultlist

def geturl(url):
    r = requests.get(url)
    return r.content


def get_URL_save_file(url, page_number):
    url_to_get = url+str(page_number)
    print(url_to_get)
    r = requests.get(url_to_get)
    # print(r.content)
    with open(f"page_{page_number}.html", "wb") as f:
        f.write(r.content)
    # soup = BeautifulSoup(r.content, 'html.parser')
    # soup = BeautifulSoup(r.content, 'lxml')

    # table = soup.find_all("table", bgcolor="#FFFFFF")
    
    # data = soup.find_all("tr",{'class':'texto'})

    # print(data)
    # print(type(data))
    # print(len(data))
    # for item in data:
    #     soup_tr = BeautifulSoup(item.text, "lxml")
    #     tds = soup.find_all("td")
    #     count = 0
    #     for td in tds:
    #         print(count, td.text)
    #         count += 1


if __name__ == "__main__":
    URLS = generate_urls(4355, 49276)
    print(f"Total to Download: {len(URLS)}")
    with ThreadPoolExecutor(max_workers=5) as executor:
        # future = executor.submit(get_URL_save_file, (2))
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(geturl, url): url for url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                print(f"Downloading {url}")
                data = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
            else:
                page_number = url[url.rfind("=") + 1:]
                with open(f"page_{page_number}.html", "wb") as f:
                    f.write(data)
                print(f"{url} downloaded.")
    print("All tasks completed!")

