
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from  ScrappedDataClean import DataClean
from DBConnection import Mongodb


class MaanNewsScraper:
    URL = 'https://www.maannews.net/'
    title =''

    @classmethod
    def get_content(cls):
        try:
            response = requests.get(MaanNewsScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            articels_info = soup.find_all('a', class_='list-1__item')
            MaanNewsScraper.title = soup.find('title').string

            articles = MaanNewsScraper.fetch_articles(articels_info)
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
        data =[]
        for pt in articels_info:
            datum = {}
            date = pt.find('span', class_='list-1__date')
            date = date.string
            datum['category']='news'
            datum['baseurl'] =MaanNewsScraper.URL
            datum['webname'] = MaanNewsScraper.title
            datum['title'] = pt['title']
            datum['url'] = pt['href']
            datum['time'] = date
            data.append(datum)
        return data

    @classmethod
    def get_covid_status(cls):
        try:
            response = requests.get(MaanNewsScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find_all('div', class_='stats__item')
            summary = MaanNewsScraper.fetch_data(div)
            #Mongodb.insert_articles(articles)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
        return summary

    @staticmethod
    def fetch_data(div):
        #data = []
        datum = {}
        for pt in div:
            status = pt.find('div', class_='stats__title').string
            val = pt.find('div', class_='stats__val').string
            datum[status]=DataClean.clean_string(val)
            
        return datum

class MaanHealthScraper:
    URL = 'https://www.maannews.net/news/health-and-life'
    title = ''

    @classmethod
    def get_content(cls):
        try:
            response = requests.get(MaanHealthScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            articels_info = soup.find_all('div', class_='column is-4')
            #print(articels_info)
            MaanHealthScraper.title = soup.find('title').string

            articles = MaanHealthScraper.fetch_articles(articels_info)
            Mongodb.insert_articles(articles)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('MaanHealthScraper Success!')
        return articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            name = pt.find('a', class_='list-6__item mt-20')
            if name:
                title = name['title']
                href = name['href']
            date = pt.find('div', class_='list-6__date')
            date = date.string
            datum['category'] = 'news'
            datum['baseurl'] = MaanHealthScraper.URL
            datum['webname'] = MaanHealthScraper.title
            datum['title'] = title
            datum['url'] = href
            datum['time'] = date
            data.append(datum)
        return data



# art = MaanNewsScraper.get_covid_status() ;print(art)
