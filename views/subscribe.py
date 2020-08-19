
from flask import Blueprint, render_template, request

from modules.CovidScraper import BBCCovidScraper, WhoCovidScraper
from connections.DBConnection import Mongodb

subscribe_blueprint = Blueprint('subscribe', __name__)


@subscribe_blueprint.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    print(request.method)
    if request.method == "POST":
        print('inside POST')
        subscribers = get_subscribers_collection()
        #subscribe_date = datetime.utcnow
        subscriber_email, subscriber_name, subscriber_website = read_form_data()

        existing_subscriber = is_subscribed(subscribers, subscriber_email)
        if existing_subscriber is None:

            add_subscriber(subscribers, subscriber_name,subscriber_email, subscriber_website)
        else:
            result = f'email {subscriber_email} Alreday sucscribed!'
            return render_template("subscribe/subscribe.html", result=result)
    else:
        result = f'email {subscriber_email} successfully sucscribed!'
        return render_template("subscribe/subscribe.html", result=result)

# def get_urls():
#     db = Mongodb.db_connect() 
#     subscribers = db['subscribers']
#     return subscribers

def get_subscribers_collection():
    db = Mongodb.db_connect()
    subscribers = db['subscribers']
    return subscribers


def is_subscribed(subscribers, subscriber_email):
    existing_subscriber = subscribers.find_one(
        {'subscriber_email': subscriber_email})
    return existing_subscriber


def read_form_data():
    subscriber_name = request.form['name']
    subscriber_email = request.form['mail']
    subscriber_website = request.form['websites']
    return subscriber_email, subscriber_name, subscriber_website


def add_subscriber(subscribers, subscriber_name, subscriber_email, subscriber_website):
    subscriber_id = subscribers.insert_one({'subscriber_name': subscriber_name,
                                            'subscriber_email': subscriber_email,
                                            'subscriber_website': subscriber_website
                                            })
    print(subscriber_id)
    new_subscriber = subscribers.find_one({'_id': subscriber_id})
    result = {'email': new_subscriber['email'] + 'successfully sucscribed!'}
