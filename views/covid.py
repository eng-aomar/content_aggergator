from flask import Flask, render_template, Blueprint


from BBCScraper import BBCScraper
from MaanScraper import MaanHealthScraper
from MOHScraper import CovidPalestine
from MaanScraper import MaanNewsScraper
import time
import concurrent.futures


from CovidScraper import BBCCovidScraper, WhoCovidScraper


covid = Blueprint('covid', __name__)


@covid.route('/covid19')
def load_covid():

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(MaanNewsScraper.get_covid_status)
        f2 = executer.submit(BBCCovidScraper.get_content)
        f3 = executer.submit(WhoCovidScraper.get_content)
        palestine_summary = f1.result()
        bbc_corona_articles = f2.result()
        who_corona_articles = f3.result()
    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")
    return render_template("covid/covid19.html",
                            palestine_summary=palestine_summary,
                            bbc_corona_articles=bbc_corona_articles,
                            who_corona_articles=who_corona_articles
                            )


