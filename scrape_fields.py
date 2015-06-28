# This script scrapes data from a website listing field categories, fields, and
# majors; used dryscrape for javascript-rendered page; works in python2.7 only

from web_list_scraper import *
import dryscrape
import re


def main():
    page = 'https://bigfuture.collegeboard.org/majors-careers'
    all_soup = get_soup_js(page)

    # get just the part of the page with majors
    root_class = 'treeview major-categories-treeview tree-root'
    major_tree = get_lists(all_soup, root_class)

    # first convert result set to soup to use generators
    major_soup = bs4.BeautifulSoup(str(major_tree))
    pretty = major_soup.prettify()
    pretty_list = [x.strip() for x in pretty.split('\n')]

    # get a list of just majors at the lowest level in the tree
    majors = []
    i = 0
    while i < len(pretty_list):
        if re.match(r'^<a', pretty_list[i]) is not None:
            majors.append(pretty_list[i + 1])
        i += 1

    # get a list of all categories, branches, and majors
    all_text = []
    for element in pretty_list:
        if element[0].isalpha():
            all_text.append(element)

    # build a dictionary of fields {major: category}
    categories = ['Arts and Humanities', 'Business', 'Health and Medicine',
                  'Multi-/Interdisciplinary Studies',
                  'Public and Social Services',
                  'Science, Math, and Technology', 'Social Sciences',
                  'Trades and Personal Services']

    category_indexes = {}
    for cat in categories:
        category_indexes[get_index(cat, all_text)] = cat

    cat_keys = sorted(category_indexes, key=category_indexes.get)

    fields = {}
    for major in majors:
        i = 0
        while i < len(cat_keys) - 1:
            if get_index(major, all_text) < cat_keys[i+1]:
                fields[major] = category_indexes[cat_keys[i]]
                i = len(cat_keys) - 1
            else:
                i += 1

    write_dict(fields, ['Major', 'Category'], 'fields.csv')


def write_dict(data_dict, fieldnames, filename):
    """Writes the contents of the dict to a csv file

    dict, list of str, str -> none"""
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for item in data_dict.items():
            writer.writerow({'Major': item[0], 'Category': item[1]})


def get_soup_js(url):
    """Returns soup from javascript-rendered webpage

    str -> soup"""
    session = dryscrape.Session()
    session.visit(url)
    response = session.body()
    soup = bs4.BeautifulSoup(response)
    return soup


def write_soup(soup, filename):
    """Writes the contents of a list to a text file

    list of str -> none"""
    with open(filename, 'w',) as file:
        file.write(str(soup))


def get_index(item, list_of_items):
    """Returns the index number of an item in a list

    obj, list -> int"""
    i = 0
    if item not in list_of_items:
        return None
    for obj in list_of_items:
        if obj == item:
            return i
        else:
            i += 1


if __name__ == '__main__':
    main()