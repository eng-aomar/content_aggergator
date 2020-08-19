import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from connections.DBConnection import Mongodb
class WafaScraper:
    URL = 'http://www.wafa.ps'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:
            response = requests.get(WafaScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            title = soup.find('title')
            WafaScraper.title = title.string
            articels_info = soup.find_all('a', class_='latestnews')
            if articels_info:
                WafaScraper.articles = WafaScraper.fetch_articles(articels_info)
                Mongodb.insert_articles(WafaScraper.articles)
            else:
                WafaScraper.get_latest_ten_articles()


            response.raise_for_status()

        except HTTPError as http_err:
            WafaScraper.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            WafaScraper.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('WafaScraper Success!')
        return WafaScraper.articles


    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            # name = pt.find(
            #     'a', {'class': 'latestnews'})
            # if name:
            url = WafaScraper.URL + pt['href']
            name = pt.string
            #date = pt.find('span', {'class': 'meta-item date'})         
            datum['category'] = 'news'
            datum['baseurl'] = WafaScraper.URL
            datum['webname'] = WafaScraper.title
            datum['title'] = name
            datum['url'] = url
            #datum['time'] = date.string
            data.append(datum)              
            # else:
            #     continue
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        WafaScraper.articles = Mongodb.find_by(
            WafaScraper.URL, db['articles'])

# art = WafaScraper.get_content()
# print(art)
