from flask import Flask, render_template, Blueprint, request
from connections.DBConnection import Mongodb
from SendEmail import MyMail

about_blueprint = Blueprint('about', __name__)


@about_blueprint.route('/about', methods=['GET', 'POST'])
def about():


    if request.method == "POST":

        print('inside POST')
        guest_full_name, guest_email, guest_phone, guest_inquiry = read_form_data()
        
        inquiries = get_inquiries_collection()
        add_inquiry(inquiries,
                    guest_full_name, guest_email, guest_phone, guest_inquiry)

        
        msg = " تم الارسال بنجاح"
        subject = f'inguiry from {guest_full_name} {guest_full_name}'
        # MyMail.send_mail(subject, guest_inquiry)

    return render_template("about/contactme.html")


def read_form_data():
    guest_full_name = request.form['fullname']
    guest_email = request.form['Email']
    guest_phone= request.form['Phone']
    guest_inquiry = request.form['subject']
    return guest_full_name, guest_email, guest_phone, guest_inquiry


def add_inquiry(inquiries, guest_full_name, guest_email, guest_phone, guest_inquiry):
    inquiry_id = inquiries.insert_one({'guest_full_name': guest_full_name,
                                       'guest_email': guest_email,
                                       'guest_phone': guest_phone,
                                       'guest_inquiry': guest_inquiry
                                        })

def get_inquiries_collection():
    db = Mongodb.db_connect()
    inquiries = db['inquiries']
    return inquiries
