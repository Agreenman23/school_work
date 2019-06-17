#Alex Greenman
#873392313
#This program utilizes the BeautifulSoup module to extract information from an
#HTML table, strip the table's information of its HTML tags, and saves it to
#a CSV file named by the user.

import requests
from bs4 import BeautifulSoup
import csv
from sys import argv

def table_to_list(table_tag):
    '''Iterates through the rows of a table, extracts every column entry from
    that row and returns the data as a list of lists, where each row is a list
    of values in the columns.'''
    #find all rows in the table tag object
    rows = table_tag.find_all('tr')
    #create an empty list to store the lists that contain column values
    contents_list=[]
    #iterate over rows, find column contents, strip them of their html tags and
    #add to list
    for row in rows:
        cols = row.find_all('td')
        cols = [guts.text.strip() for guts in cols]
        contents_list.append([guts for guts in cols if guts])

    return contents_list

def main():
    #read in each html file, create a BeautifulSoup object, and find all tables
    #in each file
    files_used = argv[1:]
    for elements in files_used:
        with open(elements) as f:
            soup2 = BeautifulSoup(f.read(), features="html.parser")
            table_tags = soup2.find_all('table')
    #iterate over all table tags in file, print first row of table, prompt user
    #for filename, if user provides filename save the table to file in csv
    #format, if no username is provided, do nothing
        i=0
        while i < len(table_tags):
            saved = table_to_list(table_tags[i])
            print(f'First Row: {saved[0]}')
            file_to_process=input("Enter a file name (or blank to skip): ")
            if file_to_process:
                with open(str(file_to_process), 'w', newline='') as example:
                    writer = csv.writer(example)
                    writer.writerows(saved)
                    i+=1
            else:
                i+=1

#run main if executed, but not if imported
if __name__ == '__main__':
   main()
