import requests
from bs4 import BeautifulSoup


def get_links(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.prettify()


URL = "https://realpython.github.io/fake-jobs/"
print(get_links(URL))

# This is not implemented in final app for now
