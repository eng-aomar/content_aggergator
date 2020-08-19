from flask import Flask, render_template

from content_aggergator.connections.DBConnection import Mongodb
from content_aggergator.views.about import about_blueprint
from content_aggergator.views.covid import covid
from content_aggergator.views.health import health_blueprint
from content_aggergator.views.home import home
from content_aggergator.views.news import news_blueprint
from content_aggergator.views.subscribe import subscribe_blueprint
from content_aggergator.views.local import local_blueprint
from content_aggergator.views.international import global_blueprint
from content_aggergator.views.jops import jobs_blueprint
from content_aggergator.views.errors_handler import errors
from content_aggergator.config import config



app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config['development'])



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
# app.config.from_object('config')
# app.config.from_object(config['development'])
# config['development'].init_app(app)


# print(f'ENV is set to: {app.config["ENV"]}')

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





