import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from connections.DBConnection import Mongodb


class PalestineTechJobs:
    URL = 'https://palestinetechjobs.com'
    title = ''
    articles = []
    @classmethod
    def get_content(cls):
        try:
            response = requests.get(PalestineTechJobs.URL)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            response.close()
            title = soup.find('title')
            PalestineTechJobs.title = title.string
            articels_info = soup.find_all('div', class_='panel_has_logo')
            #print(articels_info)
            if articels_info:

                PalestineTechJobs.articles = PalestineTechJobs.fetch_articles(
                articels_info)
                Mongodb.insert_articles(PalestineTechJobs.articles)
            else:
                PalestineTechJobs.get_latest_ten_articles()
            response.raise_for_status()

        except HTTPError as http_err:
            PalestineTechJobs.get_latest_ten_articles()
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            PalestineTechJobs.get_latest_ten_articles()
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('PalestineTechJobs Success!')
        return PalestineTechJobs.articles

    @staticmethod
    def fetch_articles(articels_info):
        data = []
        for pt in articels_info:
            datum = {}
            # , {'class': 'list-3--title list-3--row'}
            name = pt.find('a', {'class': 'panel_job_title'})
            if name:
                url = PalestineTechJobs.URL + name['href']
                name = name.string
                date = pt.find('p', {'class': 'panel_date'})
                datum['category'] = 'jobs'
                datum['baseurl'] = PalestineTechJobs.URL
                title =PalestineTechJobs.title.split('-')
                datum['webname'] = title[0]
                datum['title'] = name
                datum['url'] = url
                datum['time'] = date.string
                data.append(datum)
            else:
                continue
        return data

    @staticmethod
    def get_latest_ten_articles():
        db = Mongodb.db_connect()
        PalestineTechJobs.articles = Mongodb.find_by(JobsPS.URL, db['articles'])
# articles = PalestineTechJobs.get_content()
# print(articles)
