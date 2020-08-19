import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from connections.DBConnection import Mongodb
from ScrappedDataClean import DataClean
import pandas as pd
import lxml.html as lh

class MOHScraper:
    URL = 'http://site.moh.ps'
    title = ''

    @classmethod
    def get_content(cls):
        try:

            response = requests.get(MOHScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            articels_info = soup.find_all(
                'i', class_='fa fa-circle font-color')
 
            MOHScraper.title = soup.find('title').string
            articles = MOHScraper.fetch_articles(articels_info)
            Mongodb.insert_articles(articles)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('MOHScraper Success!')
        return articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            name = pt.find('a', {'class': 'sp-thumbnail-title'})
            if name:
                title =name.string
            link = pt.find('a')
            if link:
                href=MOHScraper.URL + link['href']
            datum['category'] = 'health'
            datum['baseurl'] = MOHScraper.URL
            datum['webname'] = MOHScraper.title
            datum['title'] = title
            datum['url'] =href
            data.append(datum)
        return data


class CovidPalestine:
    URL = 'http://site.moh.ps/index/covid19/'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:

            response = requests.get(CovidPalestine.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            covid_palestine_tables = soup.find(
                'table', class_='table table-bordered')

            CovidPalestine.title = soup.find('title').string
            print(len(covid_palestine_tables))

            table_headers= []
            # for row in covid_palestine_tables.find('tr'):
            #     print('row= ', row)
            #     for cell in row.find('th'):
            #         if cell:
            #             table_headers.append(cell.text)
            #         else:
            #             table_headers.append('المنطقة')    
                

            # for cell in row.find_all('th', class_='bg-dark text-white text-center'):
            #     print(cell)

                

            
            print(table_headers)    
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
        return covid_palestine_tables


# covid_palestine_tables = CovidPalestine.get_content()

