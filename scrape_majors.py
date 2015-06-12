#This script scrapes data from a website listing majors, schools, and degree
#programs at Indiana University Bloomington

try:
    import requests
    import bs4
    import csv
except:
    print("There was an error importing the necessary libraries.")

#BeautifulSoup objects are strings containing HTML tags and content, referred
#to as 'soup' throughout the script

def get_table_rows(url):
    """Returns soup elements with 'tr' tags

    str -> soup"""
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    return soup.select('tr')

def get_cell_info(table_cell):
    """Returns the major and program or degree if present in the table cell

    soup -> tuple of str"""
    if table_cell.contents == []:
        return ""
    else:
        try:
            #check whether the cell contains an 'a' tag
            program = table_cell.a.contents
            program[1].replace(u'\x80\x94',u' ')
            program[1].replace('â','') #this doesn't work
            return (program[0].string, program[1])
        except AttributeError:
            degree = table_cell.string
            #may not need the following line
            degree = degree.replace(u'\xa0',u' ').split(', ')
            return degree
        except:
            print("There was a problem getting the cell info.")
    
def get_row_info(table_row):
    """Returns a list of strings with program details: major, school, degrees

    soup -> list of strings"""
    row_data = table_row.select('td')
    program = []
    for cell in row_data:
        degrees = []
        info = get_cell_info(cell)
        if isinstance(info,tuple):
            major = info[0]
            school = info[1]
            program.append(major)
            program.append(school)
        elif info != '':
            for item in info:
                program.append(item)
    return program

def write_rows(table):
    """Writes the contents of the table to a csv file

    soup -> none"""
    filename = input("Please enter a name for the file to be created: ")
    with open(filename,'w', encoding='utf-8') as csvfile:
        fieldnames = ['Major','School','STEM','Degrees']
        writer = csv.DictWriter(csvfile, fieldnames)
        writer.writeheader()
        for row in table:
            info = get_row_info(row)
            temp_dict = {'Major': info[0],'STEM': '0'}
            #Note all STEM fields set to 0
            if len(info) <= 2:
                temp_dict['School'] = 'None'
                temp_dict['Degrees'] = 'None'
            else:
                temp_dict['School'] = info[1]
                degrees = info[2]
                if len(info[2:]) > 1:
                    for degree in info[3:]:
                        degrees += ', ' + degree
                temp_dict['Degrees'] = degrees
            writer.writerow(temp_dict)
            print("Program added to file: " + info[0])
              
#Creates a CSV file with the table content
page = 'http://www.iub.edu/academic/majors/all.shtml'
write_rows(get_table_rows(page))

#Need to fix get_cell_info() so that it fixes the m-dash characters that get
#incorrectly encoded
