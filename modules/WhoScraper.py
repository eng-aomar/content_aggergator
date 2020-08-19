import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from ScrappedDataClean import DataClean
from connections.DBConnection import Mongodb
class WhoScraper:
    URL = 'https://www.who.int/ar'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:

            response = requests.get(WhoScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()

            articels_info = soup.find_all(
                'div', class_='list-view--item horizontal-list-item matching-height--item')
            if articels_info:

                WhoScraper.title = DataClean.clean_string(soup.find('title').string)
                WhoScraper.articles = WhoScraper.fetch_articles(articels_info)
                Mongodb.insert_articles(WhoScraper.articles)
            else:
                WhoScraper.get_latest_ten_articles()

            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('whoScraper Success!')
        return WhoScraper.articles


    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            name = pt.find(
                'a', {'class': 'link-container'})
            if name:    
                href = name['href']
                title = name['aria-label']

            date = pt.find('span', class_='timestamp')
            date = date.string
            datum['category'] = 'health'
            datum['baseurl'] = WhoScraper.URL
            datum['webname'] = WhoScraper.title
            datum['title'] = title
            datum['url'] = href
            datum['time'] = date
            data.append(datum)
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        WhoScraper.articles = Mongodb.find_by(
            WhoScraper.URL, db['articles'])


