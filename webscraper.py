from requests import get
from bs4 import BeautifulSoup
import pandas as pd

def get_table_rows(url):

    # Send a GET request to the URL and return the .HTML page source as the variable 'page'
    page = get(url).content

    # Load the HTML in the 'page'  in BS so we can parse information out
    soup = BeautifulSoup(page, 'html.parser')

    # Isolate the HTML table as the variable table_container
    # This table contains the information we are looking to scrape
    table_container = soup.find('tbody')

    # find_all returns all the tags, as a list.
    # Exclude footer row by only returning <tr> tags with empty classes
    rows = table_container.find_all('tr', {"class": ""})

    return rows

def create_lists(rows):

    # initialize empty lists to hold scraped values
    rank = []
    name = []
    city = []

    # Iterate through each row <tr> and assign each element of <td> to a variable and append it to the list
    for row in rows:
        row_td = row.find_all('td')
        rank.append(row_td[0].get_text())
        name.append(row_td[1].get_text())
        city.append(row_td[2].get_text())

    return rank, name, city

def get_csv(rank, name, city):
    # Initialize pandas data frame and insert created lists as columns
    df = pd.DataFrame({'Rank': rank, 'Name': name, 'City':city})

    # write the pandas data frame to .CSV
    df.to_csv('output.csv')

    return df


soup = get_table_rows("https://www.4icu.org/us/")
rank, name, city = create_lists(soup)
get_csv(rank, name, city)

