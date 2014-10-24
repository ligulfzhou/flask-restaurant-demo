from threading import Thread
from flask import current_app, render_template
from flask.ext.mail import Message


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#--------------------------------------------------------------------
#here I can write dead that some one have shopped in your restaurant
#maybe I can send the time --> in the subject 


#-------------to be edited-------------------------------------------
#--------------------------------------------------------------------
def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                    sender = app.config['FLASK_MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target = send_async_email, args = [app, msg])
    thr.start()
    return thr
