import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from DBConnection import Mongodb
class WafaScraper:
    URL = 'http://www.wafa.ps'
    title =''
    @classmethod
    def get_content(cls):
        try:
            response = requests.get(WafaScraper.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            title = soup.find('title')
            WafaScraper.title = title.string
            articels_info = soup.find_all('a', class_='latestnews')
            articles = WafaScraper.fetch_articles(articels_info)
            Mongodb.insert_articles(articles)


            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('WafaScraper Success!')
        return  articles


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


# art = WafaScraper.get_content()
# print(art)
