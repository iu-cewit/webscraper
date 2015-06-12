#This script scrapes data from a website listing academic departments at
#Indiana University Bloomington

from web_list_scraper import *
#web_list_scraper requires libraries requests, bs4, and csv

page = 'http://www.iub.edu/academic/departments/index.shtml'
all_soup = get_soup(page)
depts_by_letter = get_lists(all_soup,'content-list-a-z')

all_depts = []
for letter in depts_by_letter:
    dept_list = list_items(letter)
    for dept in dept_list:
        all_depts.append(dept)

write_items(all_depts)
#user should enter filename with '.csv' extension
