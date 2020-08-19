import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from content_aggergator.connections.DBConnection import Mongodb
from content_aggergator.ScrappedDataClean import DataClean

class BBCScraper:
    URL = 'https://www.bbc.com/arabic'
    title=''
    articles =[]
    @classmethod
    def get_content(cls):
        try:

            response = requests.get(BBCScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()

            articels_info = soup.find_all(
                'a', class_='Link-sc-1dvfmi3-5 StyledLink-sc-16i2p1z-2 fdDiSd')
            if articels_info:

                BBCScraper.title = soup.find('title').string

                BBCScraper.articles = BBCScraper.fetch_articles(articels_info)
                Mongodb.insert_articles(BBCScraper.articles)
            else:
                BBCScraper.get_latest_ten_articles()
                # print(BBCScraper.articles)
                
            response.raise_for_status()

        except HTTPError as http_err:
            BBCScraper.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            BBCScraper.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
            
        else:
            print('BBCScraper Success!')
        return BBCScraper.articles

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

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        BBCScraper.articles = Mongodb.find_by(BBCScraper.URL, db['articles'])
        

# atricle = BBCScraper.get_content()
# print(atricle)


