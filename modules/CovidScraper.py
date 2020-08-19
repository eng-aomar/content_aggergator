import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from connections.DBConnection import Mongodb


class BBCCovidScraper:
    URL = 'https://www.bbc.com/arabic/51719894'
    BBC_URL = 'https://www.bbc.com'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:
            response = requests.get(BBCCovidScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            links = soup.find_all('a', class_='title-link')  # title-link
            if links:
                title = soup.find('title')
                BBCCovidScraper.title = title.string
                BBCCovidScraper.articles = BBCCovidScraper.fetch_articles(links)
                Mongodb.insert_articles(BBCCovidScraper.articles)
            else:
                BBCCovidScraper.get_latest_ten_articles()
            response.raise_for_status()

        except HTTPError as http_err:
            BBCCovidScraper.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            BBCCovidScraper.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('BBCCovidScraper Success!')
        return BBCCovidScraper.articles

    @staticmethod
    def fetch_articles(links):
        data = []
        for pt in links:
            datum = {}
            name = pt.find(
                'span', {'class': 'title-link__title-text'})
            if name:
                url = BBCCovidScraper.BBC_URL + pt['href']
                name = name.string
                #date = pt.find('span', {'class': 'meta-item date'})
                title =BBCCovidScraper.title.split('-')
                datum['category'] = 'covid'
                datum['baseurl'] = BBCCovidScraper.URL
                datum['webname'] = title[0] 
                datum['title'] = name
                datum['url'] = url
                #datum['time'] = date.string
                data.append(datum)
            else:
                continue
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        BBCCovidScraper.articles = Mongodb.find_by(
                                                BBCCovidScraper.URL,
                                                db['articles'])

class WhoCovidScraper:
    URL = 'https://www.who.int/ar/emergencies/diseases/novel-coronavirus-2019'
    WHO_URL = 'https://www.who.int/ar/'
    title = ''
    articles = []

    @classmethod
    def get_content(cls):
        try:
            response = requests.get(WhoCovidScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            links = soup.find_all(
                'a', class_='link-container')  # link-container
            if links:
                title = soup.find('title')
                WhoCovidScraper.title = title.string
                WhoCovidScraper.articles = WhoCovidScraper.fetch_articles(links)
                Mongodb.insert_articles(WhoCovidScraper.articles)
            else:
                WhoCovidScraper.get_latest_ten_articles()
            response.raise_for_status()
        except HTTPError as http_err:
            WhoCovidScraper.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            WhoCovidScraper.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('WhoCovidScraper Success!')
        return WhoCovidScraper.articles

    @staticmethod
    def fetch_articles(links):
        data = []
        for pt in links:
            datum = {}
            name = pt.find(
                'p', {'class': 'heading text-underline'})
            if name:
                url =  pt['href']
                name = name.string
                #date = pt.find('span', {'class': 'timestamp'})
                datum['category'] = 'covid'
                datum['baseurl'] = WhoCovidScraper.URL
                datum['webname'] = WhoCovidScraper.title
                datum['title'] = name
                datum['url'] = url
                #datum['time'] = date.string
                data.append(datum)
            else:
                continue
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        WhoCovidScraper.articles = Mongodb.find_by(
            WhoCovidScraper.URL,
            db['articles'])

# articles = BBCCovidScraper.get_content()
# print(articles)
