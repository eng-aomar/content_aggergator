from flask import Flask, render_template, Blueprint
from requests.exceptions import HTTPError

from modules.WhoScraper import WhoScraper
from modules.MaanScraper import MaanHealthScraper
from modules.MOHScraper import MOHScraper
from modules.CovidScraper import BBCCovidScraper, WhoCovidScraper
import concurrent.futures
import time
health_blueprint = Blueprint('health', __name__)


@health_blueprint.route('/health')
def health():

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(WhoScraper.get_content)
        f2 = executer.submit(MaanHealthScraper.get_content)
        f3 = executer.submit(WhoCovidScraper.get_content)
        f4 = executer.submit(BBCCovidScraper.get_content)
        who_articles = f1.result()
        maan_health = f2.result()
        moh_articles = f3.result()
        bbc_health = f4.result()
    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")
    return render_template("health/health.html",
                           who_articles=who_articles,
                           maan_health=maan_health,
                           moh_articles=moh_articles,
                           bbc_health=bbc_health)
