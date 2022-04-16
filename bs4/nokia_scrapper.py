from bs4 import BeautifulSoup
from lxml import etree
import requests
import colorama
from colorama import Fore
from datetime import datetime
import pandas as pd , numpy as np 

import warnings
warnings.filterwarnings("ignore")

# creating the list of dates 
list_of_dates = []

try:
    #taking input from user
#     start_date = input("Enter start date (in YYYY MM DD) : " )
#     end_date = input("Enter end date (in YYYY MM DD) : " )
    end_date = '2022 4 16'
    start_date = '2022 3 25'

    #adding up condition 
    if start_date > end_date :
        print(Fore.RED+ '\nstart date must come before end date')

    #appending to the list includes both dates
    else:
        for d in pd.date_range(start_date, end_date,inclusive="both"):
            list_of_dates.append(d.strftime("%#d %b %Y"))

#dealing with error/s    
except ValueError:
    print(Fore.RED +"\nAdd the dates in correct format (in YYYY MM DD)")


#deciding how many pages to scrape
if len(list_of_dates) <= 6:
    factor = len(list_of_dates)
else:
    factor = len(list_of_dates)/6

print(f"scrapping {int(factor)} pages")


#there are 142 pages

titles = []
dates = []
links = []

try:
    
    for page_number in range(int(factor)):
#     for page_number in range(3):
        #getting the urls
        url =  f'https://www.nokia.com/about-us/newsroom/press-and-stock-exchange-releases/?page={page_number}/'

        #parsing
        source = requests.get(url)
        soup = BeautifulSoup(source.content,'lxml')

        try:
            #creating container and fetching the data
            all_containers = soup.findAll('div', {'class' :'views-row'})
            for container in all_containers:
                published_date = container.find('label').text
                
                if published_date in list_of_dates:
                    link = container.find('a')['href']
                    title = container.find('h3').text
                    dates.append(published_date)
                    titles.append(title)
                    links.append("https://www.nokia.com" + link)

            print(f"scrapping done for page {page_number}\n")
            
        except:
            pass
except:
    pass

#zippling the list so that it'll form the tuple
zipped = list(zip(dates,titles,links))

#creating the csv 
temp_csv = pd.DataFrame(zipped,columns=['date','title','link'])

articles = []

for link_number in range(len(temp_csv)):
    
    #getting the url from data
    url = temp_csv['link'][link_number]
    
    #parsing
    source = requests.get(url)
    soup = BeautifulSoup(source.content,'lxml')
     
    try:    
        #creating container and fetching the data    
        all_containers = soup.findAll('div',{'class' :"main-content-region"})

        for container in all_containers:
            article = container.text
            articles.append(article)

        print(f"scrapping done for url {link_number}\n")
        
    except:
        pass

temp_csv['article'] = articles

#to csv
temp_csv.to_csv('bs4 generated nokia.csv')

#to json
temp_csv.to_json('bs4 generated nokia.json')