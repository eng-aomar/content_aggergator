

from flask import Flask, render_template, request, url_for, Blueprint


from modules.BBCScraper import BBCScraper
from modules.RTScraper import RTScraper
from modules.WhoScraper import WhoScraper
from connections.DBConnection import Mongodb
from modules.CovidScraper import BBCCovidScraper
import time
import concurrent.futures

global_blueprint = Blueprint('global', __name__)


@global_blueprint.route('/global')
def load_global():
    start = time.perf_counter()
    rt_articles, who_articles, bbc_articles, bbc_health = get_data()
    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")
    return render_template("global/global.html",
                           rt_articles=rt_articles,
                           who_articles=who_articles,
                           bbc_articles=bbc_articles,
                           bbc_health=bbc_health
                           )


def get_data():

    
    bbc_health = BBCCovidScraper.get_content()
    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(RTScraper.get_content)
        f2 = executer.submit(WhoScraper.get_content)
        f3 = executer.submit(BBCScraper.get_content)
        f4 = executer.submit(BBCCovidScraper.get_content)
    rt_articles = f1.result()
    who_articles = f2.result()
    bbc_articles = f3.result()

    return  rt_articles, who_articles, bbc_articles, bbc_health

