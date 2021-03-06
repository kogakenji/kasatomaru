import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import db

URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Provincia=999&Navio=999&AnoChegada=999&Idioma=P"
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=2&PAG=T
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=1&PAG=F
# http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=2&PAG=F
FINAL_URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Navio=999&AnoChegada=999&Provincia=999&Idioma=P&Busca=&PAGATUAL=49276&PAG=F"
# Last page = 49276
INITIAL_URL = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Provincia=999&Busca=&Idioma=P&PAGATUAL="
INITIAL_URL_JP = "http://www.museubunkyo.org.br/ashiato/web2/ListaFamilia.asp?Provincia=999&Busca=&Idioma=J&PAGATUAL="


def get_jp_files():
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f.strip('.html').lstrip('page_') for f in listdir("../jp_files/jp") if isfile(join("../jp_files/jp", f))]
    print(f"Size of jp folder {len(onlyfiles)}")
    return onlyfiles


def generate_urls(start, end):
    """Generate url list with given start and end of indexes"""
    resultlist = []

    downloaded_files = get_jp_files()
    for i in range(start, end):
        if str(i) not in downloaded_files:
            print(f"adding {i}")
            resultlist.append(INITIAL_URL+str(i))
    return resultlist

def geturl(url):
    """Get the content of a web page"""
    r = requests.get(url)
    return r.content


def get_main_pages():
    """Generates urls based on indexes and downloads using threads"""
    URLS = generate_urls(1, 49276)
    print(f"Total generated: {len(URLS)}")
    print(URLS)


    with ThreadPoolExecutor(max_workers=5) as executor:
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
                with open(f"../jp_files/jp/page_{page_number}.html", "wb") as f:
                    f.write(data)
                    print(f"wrote page to {f}")
                print(f"{url} downloaded.")
    print("All tasks completed!")

def get_family_pages():
    """Get urls in database, downloads the pages of families"""
    URLS = db.families()
    print(f"Total to Download: {len(URLS)}")
    with ThreadPoolExecutor(max_workers=2) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(geturl, url): url for _, url in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                print(f"Downloading {url}")
                data = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
            else:
                page_number = url[url.find("=")+1:url.find("&")]
                # write data to a file
                with open(f"page_{page_number}.html", "wb") as f:
                    f.write(data)
                print(f"{url} downloaded.")
    print("All tasks completed!")

if __name__ == "__main__":
    # get the main pages of people
    get_main_pages()
    # get_family_pages()
