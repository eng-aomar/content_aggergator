import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from ScrappedDataClean import DataClean
from DBConnection import Mongodb
class RTScraper:
    URL = 'https://arabic.rt.com'
    title = ''

    @classmethod
    def get_content(cls):
        try:

            response = requests.get(RTScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            articels_info = soup.find('ul', {'class': 'last-news_list'})     
            RTScraper.title = soup.find('title').string
            articles = RTScraper.fetch_articles(articels_info)
            Mongodb.insert_articles(articles)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
        return  articles

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

articles= RTScraper.get_content()
