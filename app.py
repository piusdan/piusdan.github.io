import os

from dotenv import load_dotenv

from flask import Flask
from flask import render_template, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, validators

load_dotenv()

app = Flask(__name__)

config = dict(
    SECRET_KEY=os.getenv("FLASK_SECRET", "secret"),
    ADMIN_MAIL=os.getenv("ADMIN_MAIL"),
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_DEFAULT_SENDER="noreply@piusdan.me",
)
app.config.from_mapping(
    config
)

# Initialize extensions
mail = Mail(app)


# forms
class ContactForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25), validators.DataRequired()], description='Your Name')
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
    phone = StringField('Phone Number', [validators.DataRequired()])
    message = TextAreaField('Message', [validators.Length(min=10, max=200), validators.DataRequired()])


def send_mail(message, name, phone, email):
    msg = Message(recipients=[app.config["ADMIN_MAIL"]])
    subject = f"[Personal Website] New Message from {name}"
    msg.subject = subject
    msg.body = f'{message}\nPhone: {phone}\nEmail: {email}'
    msg.html = f'<p>{message}</p><p>Phone: {phone}<br/>Email: {email}</p>'
    mail.send(msg)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            send_mail(email=form.email.data, name=form.name.data, message=form.message.data, phone=form.phone.data)
        except Exception as exc:
            app.logger.error(f"Encountered error sending mail {exc}")

        flash('Message sent. Pius will be notified soon!')
        return redirect(url_for('.index'))
    return render_template("index.html", form=form)
