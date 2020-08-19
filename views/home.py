

from flask import Flask, render_template, request, url_for, Blueprint


from content_aggergator.modules.BBCScraper import BBCScraper
from content_aggergator.modules.MaanScraper import MaanNewsScraper, MaanHealthScraper
from content_aggergator.modules.MOHScraper import MOHScraper, CovidPalestine
from content_aggergator.modules.RTScraper import RTScraper
from content_aggergator.modules.WafaScraper import WafaScraper
from content_aggergator.modules.WhoScraper import WhoScraper
from content_aggergator.connections.DBConnection import Mongodb

from content_aggergator.modules.CovidScraper import BBCCovidScraper, WhoCovidScraper

import time
import concurrent.futures


home = Blueprint('index', __name__)



@home.route('/')
@home.route('/index')
@home.route('/home')
def load_home():
    start = time.perf_counter()
    wafa_articles, maan_articles, rt_articles, moh_articles, who_articles, bbc_articles, maan_health, bbc_health = get_data()

    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")
    
    return render_template("home/index.html",
                            wafa_articles=wafa_articles,
                            maan_articles=maan_articles,
                            rt_articles=rt_articles,
                            moh_articles=moh_articles,
                            who_articles=who_articles,
                            bbc_articles=bbc_articles,
                            maan_health=maan_health,
                            bbc_health=bbc_health
                            )

def get_data():
    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(WafaScraper.get_content)
        f2 = executer.submit(MaanNewsScraper.get_content)
        f3 = executer.submit(RTScraper.get_content)
        f4 = executer.submit(WhoCovidScraper.get_content)
        f5 = executer.submit(WhoScraper.get_content)
        f6 = executer.submit(BBCScraper.get_content)
        f7 = executer.submit(MaanHealthScraper.get_content)
        f8 = executer.submit(BBCCovidScraper.get_content)
        wafa_articles = f1.result()
        maan_articles = f2.result()
        rt_articles = f3.result()
        moh_articles = f4.result()
        who_articles = f5.result()
        bbc_articles = f6.result()
        maan_health = f7.result()
        bbc_health = f8.result()

    return wafa_articles, maan_articles, rt_articles, moh_articles, who_articles, bbc_articles, maan_health, bbc_health
                            



