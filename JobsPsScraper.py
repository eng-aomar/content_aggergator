import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from DBConnection import Mongodb


class JobsPS:
    URL = 'https://www.jobs.ps/'
    title = ''

    @classmethod
    def get_content(cls):
        try:
            response = requests.get(JobsPS.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            title = soup.find('title')
            JobsPS.title = title.string
            articels_info = soup.find_all('a', class_='list-3--title list-3--row')
            #print(articels_info)
            articles = JobsPS.fetch_articles(articels_info)
            Mongodb.insert_articles(articles)

            response.raise_for_status()

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('JobsPS Success!')
        return articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            url = JobsPS.URL + pt['href']
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

# articles = JobsPS.get_content()
# print(articles)
