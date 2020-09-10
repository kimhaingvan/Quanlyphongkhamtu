import smtplib

from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config.from_object('config')
db = SQLAlchemy(app)
smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
admin = Admin(app=app, name='QUAN LY PHONG KHAM TU', template_mode='bootstrap3',index_view=AdminIndexView(name="Trang chủ"))
login = LoginManager(app=app)
