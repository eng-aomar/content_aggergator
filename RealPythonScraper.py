import requests
from bs4 import BeautifulSoup
from flask import request
# try:
articel = {}
    # 'https://api.github.com', 'https://api.github.com/invalid',
for url in ['https://realpython.com/']:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        divs = soup.find_all('div', class_='card-body m-0 p-0 mt-2')
        
        user_agent = request.headers.get('User-Agent')
        print(user_agent)
        for div in divs:
            articel_title = div.find(
                    'h2', {'class': 'card-title h4 my-0 py-0'})
            link = div.find('a')
            if link.has_attr('href'):
                article_link = link['href']

            articel[article_link] = articel_title
            response.raise_for_status()

#     except HTTPError as http_err:
#         print(f'HTTP error occurred: {http_err}')  # Python 3.6
#     except Exception as err:
#         print(f'Other error occurred: {err}')  # Python 3.6
#     else:
#         print('Success!')
# # return render_template("homepage.html", titles=articel, url=url)

