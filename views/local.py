from flask import Flask, render_template, Blueprint
from requests.exceptions import HTTPError

from MOHScraper import MOHScraper
from MaanScraper import MaanHealthScraper, MaanNewsScraper
from WafaScraper import WafaScraper
from PalestineTechJobsScraper import PalestineTechJobs
from  JobsPsScraper import JobsPS
import time
import concurrent.futures

local_blueprint = Blueprint('local', __name__)


@local_blueprint.route('/local')
def local():
    start = time.perf_counter()
    wafa_articles, maan_articles, moh_articles, jobs_articles, tech_jobs_articles, maan_health = get_data()
    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")
    return render_template("local/local.html",
                        wafa_articles=wafa_articles,
                        maan_articles=maan_articles,
                        moh_articles=moh_articles,
                        jobs_articles=jobs_articles,
                        tech_jobs_articles=tech_jobs_articles,
                        maan_health=maan_health
                        )


def get_data():
    

    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(WafaScraper.get_content)
        f2 = executer.submit(MaanNewsScraper.get_content)
        f3 = executer.submit(MOHScraper.get_content)
        f4 = executer.submit(JobsPS.get_content)
        f5 = executer.submit(PalestineTechJobs.get_content)
        f6 = executer.submit(MaanHealthScraper.get_content)
        wafa_articles =f1.result()
        maan_articles = f2.result()
        moh_articles = f3.result(0)
        jobs_articles = f4.result()
        tech_jobs_articles = f5.result()
        maan_health = f6.result()
    return wafa_articles, maan_articles,  moh_articles, jobs_articles, tech_jobs_articles, maan_health