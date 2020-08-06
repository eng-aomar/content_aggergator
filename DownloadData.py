
from DBConnection import Mongodb 
import csv
import ast
import pandas as pd
db = Mongodb.db_connect()
articles_collection = db['articles']
baeurl = 'http://www.wafa.ps'

all_articles = Mongodb.find_by(baeurl, articles_collection)
dictionary_articles = ast.literal_eval(all_articles)

# with open('articels.csv', 'w') as scvfile:
#     header_fields = ('_id','category', 'baseurl', 'title', 'url', 'time')
    
#     the_writer = csv.DictWriter(scvfile, header_fields)
#     the_writer.writeheader

#     for article in dictionary_articles:
#         the_writer.writerow(article)


df = pd.DataFrame(list(all_articles))
df.to_csv('csvfile.csv', index=False, encoding='utf-8')
