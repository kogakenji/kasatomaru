import requests
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import db
import os

START = 1
END = 24567
PORTUGUESE = "p"
JAPANESE = "j"
FAMILY = "f"
PORTUGUESE_PATH = "../files/pt"
JAPANESE_PATH = "../files/jp"
FAMILY_PATH = "../files/family"

def get_downloaded(language, language_path):
    path_exists = False
    if language == PORTUGUESE:
        path_exists = os.path.exists(PORTUGUESE_PATH)
        if not path_exists:
            os.makedirs(PORTUGUESE_PATH)
    elif language == JAPANESE:
        path_exists = os.path.exists(JAPANESE_PATH)
        if not path_exists:
            os.makedirs(JAPANESE_PATH)
    elif language == FAMILY:
        path_exists = os.path.exists(FAMILY_PATH)
        if not path_exists:
            os.makedirs(FAMILY_PATH)

    from os import listdir
    from os.path import isfile, join
    onlynum = [f.strip('.html').lstrip('page_') for f in listdir(language_path) if isfile(join(language_path, f))]
    print(f"Size of folder {len(onlynum)}")
    return onlynum


def generate_urls(start, end, language):
    """Generate url list with given start and end of indexes"""
    resultlist = []
    downloaded = None
    if language == PORTUGUESE:
        downloaded = get_downloaded(language, PORTUGUESE_PATH)
    elif language == JAPANESE:
        downloaded = get_downloaded(language, JAPANESE_PATH)

    for page in range(start, end):
        if str(page) not in downloaded:
            dict_page = {"page": page,
            "url": f"http://imigrantes.ubik.com.br/Busca/ListaFamilias?page={page}&Lingua={language}&Ordenar=Partida"
            }
            resultlist.append(dict_page)
    return resultlist

def geturl(page):
    """Get the content of a web page"""
    r = requests.get(page["url"])
    return r.content, page["page"]


def get_main_pages(LANGUAGE):
    """Generates urls based on indexes and downloads using threads"""
    URLS = generate_urls(START, END, LANGUAGE)
    print(f"Total generated: {len(URLS)}")
    # print(f"example: {URLS[0]['url']}")
        
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(geturl, page): page for page in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                print(f"Downloading: {url}")
                data, page = future.result()
                # print(f"data got: {data}")
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
            else:
                write_file(LANGUAGE, page, data)
    print("All tasks completed!")


def write_file(language, page, data):
    if language == PORTUGUESE:
        with open(f"{PORTUGUESE_PATH}/page_{page}.html", "wb") as f:
            f.write(data)
    elif language == JAPANESE:
        with open(f"{JAPANESE_PATH}/page_{page}.html", "wb") as f:
            f.write(data)
    elif language == FAMILY:
        with open(f"{FAMILY_PATH}/page_{page}.html", "wb") as f:
            f.write(data)


def get_family_pages():
    """Get urls in database, downloads the pages of families"""
    downloaded = get_downloaded(FAMILY, FAMILY_PATH)
    URLS = []
    for page, url in db.families():
        if str(page) not in downloaded:
            URLS.append({"page": page,
                        "url": url})
    
    print(f"Total to Download: {len(URLS)}")
    with ThreadPoolExecutor(max_workers=5) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = {executor.submit(geturl, page): page for page in URLS}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                print(f"Downloading {url}")
                data, page = future.result()
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
            else:
                # write data to a file
                write_file(FAMILY, page, data)
    print("All tasks completed!")

if __name__ == "__main__":
    # get the main pages of people
    # 1) get the main pages of portuguese language
    # get_main_pages(PORTUGUESE)
    # 2) get the main pages of japanese language
    # get_main_pages(JAPANESE)
    # 3) get the family pages
    get_family_pages()
