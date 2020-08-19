from flask import Flask, render_template, Blueprint
from requests.exceptions import HTTPError

from modules.PalestineTechJobsScraper import PalestineTechJobs
from modules.JobsPsScraper import JobsPS
import time
import threading

import concurrent.futures

jobs_blueprint = Blueprint('jobs', __name__)


@jobs_blueprint.route('/jobs')
def jobs():
    start = time.perf_counter()
    
    with concurrent.futures.ThreadPoolExecutor() as executer:
        f1 = executer.submit(JobsPS.get_content)
        f2 = executer.submit(PalestineTechJobs.get_content)
        jobs_articles=f1.result()
        tech_jobs_articles = f2.result()
        
        

    finish = time.perf_counter()  # end timer
    print(f"Finished in {round(finish-start,2)} seconds")

    return render_template("jobs/jobs.html",
                           jobs_articles=jobs_articles,
                           tech_jobs_articles=tech_jobs_articles
                           )
