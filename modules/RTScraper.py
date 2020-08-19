import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from ScrappedDataClean import DataClean
from connections.DBConnection import Mongodb
class RTScraper:
    URL = 'https://arabic.rt.com'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:

            response = requests.get(RTScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            articels_info = soup.find('ul', {'class': 'last-news_list'})
            if articels_info:
                RTScraper.title = soup.find('title').string
                RTScraper.articles = RTScraper.fetch_articles(articels_info)
                Mongodb.insert_articles(RTScraper.articles)
            else:
                RTScraper.get_latest_ten_articles()
            response.raise_for_status()
        except HTTPError as http_err:
            RTScraper.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            RTScraper.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('RTScraper Success!')
        return RTScraper.articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            name = pt.find('span')
            link = pt.find('a')
            href=link['href']
            date = pt.find('time')
            date = DataClean.clean_string(date.string)
            datum['category'] = 'news'
            datum['baseurl'] = RTScraper.URL
            datum['webname'] = DataClean.clean_string(RTScraper.title)
            datum['title'] = name.string
            datum['url'] = RTScraper.URL + href
            datum['time'] = date
            data.append(datum)
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        RTScraper.articles = Mongodb.find_by(
            RTScraper.URL, db['articles'])
