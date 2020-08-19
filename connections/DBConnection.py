from pymongo import MongoClient
import os

class Mongodb:
    
    @classmethod
    def db_connect(cls):
        DB_URI = os.environ.get('DB_URI')
        #print(DB_URI) os.environ.get('DB_URI')
        client = MongoClient(DB_URI)
        db = client.contentagregatordb
        return db

    @classmethod
    def get_urls(cls):
        db = Mongodb.db_connect()
        website_collection = db['websites']
        websites = website_collection.find()
        return websites

    @classmethod
    def get_url_by(cls, url_category):
        db = Mongodb.db_connect()
        website_collection = db['websites']
        websites = website_collection.find(url_category)
        return websites

    @classmethod
    def get_articels_collection(cls):
        db = Mongodb.db_connect()
        return db['articles']

    @classmethod
    def is_saved_to(cls, articles_collection, article_url):
        article_found = articles_collection.find_one({'url': article_url})
        return article_found

    @classmethod
    def insert_articles(cls,articles):
        articles_collection = Mongodb.get_articels_collection()

        for article in articles:
            article_found = Mongodb.is_saved_to(articles_collection,
                                                article['url'])
            if article_found is None:

                articles_collection.insert_one(article)
            else:
                pass

    @classmethod
    def find_by(cls, baseurl, articles_collection):
        all_article = articles_collection.find({'baseurl': baseurl}, sort=[('_id', -1)]).limit(10)
        data =[]
        for x in all_article:
            datum = {}
            datum['category'] = x['category']
            datum['baseurl'] = x['baseurl']
            datum['webname'] = x['webname']
            datum['title'] = x['title']
            datum['url'] = x['url']
            data.append(datum)
        return data

# db = Mongodb.db_connect() 
# latest_articles = Mongodb.find_by('https://www.bbc.com/arabic', db['articles'])
# print(latest_articles)


