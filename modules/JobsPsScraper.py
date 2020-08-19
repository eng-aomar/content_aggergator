import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from connections.DBConnection import Mongodb


class JobsPS:
    URL = 'https://www.jobs.ps/'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:
            response = requests.get(JobsPS.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            title = soup.find('title')
            JobsPS.title = title.string
            articels_info = soup.find_all(
                'a', class_='list-3--title list-3--row')
            #print(articels_info) list-3--title list-3--row
            if articels_info:
                JobsPS.articles = JobsPS.fetch_articles(articels_info)
                Mongodb.insert_articles(JobsPS.articles)
            else:
                JobsPS.get_latest_ten_articles()
            response.raise_for_status()

        except HTTPError as http_err:
            JobsPS.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            JobsPS.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('JobsPS Success!')
        return JobsPS.articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            url =  pt['href']
            name = pt['title']
            datum['category'] = 'jobs'
            datum['baseurl'] = JobsPS.URL
            title = JobsPS.title.split('-')
            datum['webname'] = title[0] + '-' + title[1]
            datum['title'] = name
            datum['url'] = url
                #datum['time'] = date.string
            data.append(datum)
            
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        JobsPS.articles = Mongodb.find_by(JobsPS.URL, db['articles'])

# articles = JobsPS.get_content()
# print(articles)
