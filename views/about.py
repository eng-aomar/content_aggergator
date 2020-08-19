from flask import Flask, render_template, Blueprint, request
from content_aggergator.connections.DBConnection import Mongodb
from content_aggergator.SendEmail import MyMail

about_blueprint = Blueprint('about', __name__)


@about_blueprint.route('/about', methods=['GET', 'POST'])
def about():


    if request.method == "POST":

        print('inside POST')
        guest_first_name, guest_last_name, guest_inquiry = read_form_data()
        
        inquiries = get_inquiries_collection()
        add_inquiry(inquiries,
                            guest_first_name,
                            guest_last_name, guest_inquiry)

        
        msg = " تم الارسال بنجاح"
        subject = f'inguiry from {guest_first_name} {guest_last_name}'
        MyMail.send_mail(subject, guest_inquiry)

    return render_template("about/about.html")


def read_form_data():
    guest_first_name = request.form['firstname']
    guest_last_name = request.form['lastname']
    guest_inquiry = request.form['subject']
    return guest_first_name, guest_last_name, guest_inquiry

def add_inquiry(inquiries,guest_first_name, guest_last_name, guest_inquiry):
    inquiry_id = inquiries.insert_one({'guest_first_name': guest_first_name,
                                        'guest_last_name': guest_last_name,
                                        'guest_inquiry': guest_inquiry
                                        })

def get_inquiries_collection():
    db = Mongodb.db_connect()
    inquiries = db['inquiries']
    return inquiries
