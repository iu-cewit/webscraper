#This script provides functions for scraping text data from lists on websites

try:
    import requests
    import bs4
    import csv
except:
    print("There was an error importing the necessary libraries.")

#BeautifulSoup objects are strings containing HTML tags and content, referred
#to as 'soup' throughout the script

def get_soup(url):
    """Returns soup from webpage

    str -> soup"""
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    return soup

def get_lists(soup,html_class=''):
    """Returns list of soup elements with 'ul' tag and given class

    soup, str -> list of soups"""
    if html_class == '':
        return soup.find_all('ul')
    else:
        return soup.find_all('ul', html_class)

def list_items(soup):
    """Returns a list of strings with items from unordered list

    soup -> list of str"""
    contents = str(soup.text)
    items = contents.split(sep='\n')
    for item in items.copy():
        if item == '' or '(see ' in item:
            items.remove(item)
            #not sure why list includes empty strings
        elif ',' in item:
            text = item.split(sep=', ')
            items.remove(item)
            items.append(text[1] + ' ' + text[0])
            #fixes 'lastname, firstname' convention
    return items

def write_items(item_list):
    """Writes the contents of a list to a csv file

    list of str -> none"""
    filename = input("Please enter a name for the file to be created: ")
    with open(filename, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in item_list:
            writer.writerow([item])
            #without brackets around item, the writer object splits each word
            #into individual characters separated by commas
