from flask_mail import Message,Mail
from flask import render_template
from . import mail


def mail_message(subject,template,to,**kwargs):
    subject_pref = 'DailyBlog'
    sender_email = 'testingemailpk6@gmail.com'

    email = Message(subject_pref+subject, sender=sender_email, recipients=[to])
    email.body= render_template(template + ".txt",**kwargs)
    email.html = render_template(template + ".html",**kwargs)
    mail.send(email)