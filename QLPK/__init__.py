from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "SERECT-KEY-IS-SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/flaskmysql123"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db = SQLAlchemy(app)
admin = Admin(app=app, name='QUAN LY PHONG KHAM TU', template_mode='bootstrap3',index_view=AdminIndexView(name="Trang chủ"))
login = LoginManager(app=app)
