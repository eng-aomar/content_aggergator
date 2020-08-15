import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from DBConnection import Mongodb
from ScrappedDataClean import DataClean

class BBCScraper:
    URL = 'https://www.bbc.com/arabic'
    title=''

    @classmethod
    def get_content(cls):
        try:

            response = requests.get(BBCScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()

            articels_info = soup.find_all(
                'a', class_='Link-sc-1dvfmi3-5 StyledLink-sc-16i2p1z-2 fdDiSd')
            #print(articels_info)
 
            BBCScraper.title = soup.find('title').string


            articles = BBCScraper.fetch_articles(articels_info)
            Mongodb.insert_articles(articles)
            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
        return articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            if pt.string:
                title = pt.string
                href='https://www.bbc.com' + pt['href']
                
                datum['category'] = 'news'
                datum['baseurl'] = BBCScraper.URL
                datum['webname'] = BBCScraper.title
                datum['title'] = title
                datum['url'] = href
            else:
                continue    

            data.append(datum)
        return data


# atricle = BBCScraper.get_content()
# print(atricle)
