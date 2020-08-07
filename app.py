from flask import Flask

from DBConnection import Mongodb
from views.about import about_blueprint
from views.covid import covid
from views.health import health_blueprint
from views.home import home
from views.news import news_blueprint
from views.subscribe import subscribe_blueprint
from views.local import local_blueprint
from views.international import global_blueprint
from views.jops import jobs_blueprint
from config import config


app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(home)
app.register_blueprint(news_blueprint)
app.register_blueprint(about_blueprint)
app.register_blueprint(covid)
app.register_blueprint(subscribe_blueprint)
app.register_blueprint(health_blueprint)
app.register_blueprint(local_blueprint)
app.register_blueprint(global_blueprint)
app.register_blueprint(jobs_blueprint)

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


