import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from DBConnection import Mongodb


class PalestineTechJobs:
    URL = 'https://twitter.com/PrograminLovers'
    title = ''

    @classmethod
    def get_content(cls):
        try:
            response = requests.get(PalestineTechJobs.URL)
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('title')
            PalestineTechJobs.title = title.string
            articels_info = soup.find_all('div', class_='panel_has_logo')
            #print(articels_info)
            articles = PalestineTechJobs.fetch_articles(articels_info)
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
                datum['webname'] = PalestineTechJobs.title
                datum['title'] = name
                datum['url'] = url
                datum['time'] = date.string
                data.append(datum)
            else:
                continue
        return data

# articles = PalestineTechJobs.get_content()
# print(articles)
