from flask import Flask, render_template

from connections.DBConnection import Mongodb
from views.about import about_blueprint
from views.covid import covid
from views.health import health_blueprint
from views.home import home
from views.news import news_blueprint
from views.subscribe import subscribe_blueprint
from views.local import local_blueprint
from views.international import global_blueprint
from views.jops import jobs_blueprint
from views.errors_handler import errors
from config import config



app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config['production'])



app.register_blueprint(home)
app.register_blueprint(news_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(covid)
app.register_blueprint(subscribe_blueprint)
app.register_blueprint(health_blueprint)
app.register_blueprint(local_blueprint)
app.register_blueprint(global_blueprint)
app.register_blueprint(jobs_blueprint)
app.register_blueprint(errors)


@app.context_processor
def load_menus():
    db = Mongodb.db_connect()
    menus_collection = db['menus']
    menus = menus_collection.find()
    menus_items = {}
    for menu in menus:
        page = menu['menu_page']
        name = menu['menu_name']
        menus_items.update({page: name})
    return {'menus_items': menus_items}





