from flask import Flask, render_template, Blueprint
from requests.exceptions import HTTPError

from modules.BBCScraper import BBCScraper
from modules.MaanScraper import MaanNewsScraper
from modules.RTScraper import RTScraper
from modules.WafaScraper import WafaScraper
import time
import concurrent.futures


news_blueprint = Blueprint('news', __name__)


@news_blueprint.route('/news')
def news():
    start = time.perf_counter()

    wafa_articles = WafaScraper.get_content()
    maan_articles = MaanNewsScraper.get_content()
    rt_articles = RTScraper.get_content()
    bbc_articles = BBCScraper.get_content()

    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(WafaScraper.get_content)
        f2 = executer.submit(MaanNewsScraper.get_content)
        f3 = executer.submit(RTScraper.get_content)
        f4 = executer .submit(BBCScraper.get_content)
        wafa_articles = f1.result()
        maan_articles = f2.result()
        rt_articles = f3.result()
        bbc_articles = f4.result()
    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")
    return render_template("news/news.html",
                            wafa_articles=wafa_articles,
                            maan_articles=maan_articles,
                            rt_articles=rt_articles,
                            bbc_articles=bbc_articles)



