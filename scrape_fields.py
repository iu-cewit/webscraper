# This script scrapes data from a website listing field categories, fields, and
# majors; install requirements before sourcing script

from web_list_scraper import *
import dryscrape

def main():
    page = 'https://bigfuture.collegeboard.org/majors-careers'
    all_soup = get_soup_js(page)
    print(all_soup)

def get_soup_js(url):
    """Returns soup from javascript-rendered webpage

    str -> soup"""
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    soup = bs4.BeautifulSoup(response)
    return soup


if __name__ == '__main__':
    main()