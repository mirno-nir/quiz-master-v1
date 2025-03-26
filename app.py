# https://docs.google.com/document/d/e/2PACX-1vQ9bIdyfpUwdevF2bRSPGsFIGKfxaw9tytEyK2bZixrGgPKHMFFajBm8f_MZ7faTfjCdCH0d0_QvDau/pub 

from flask import Flask
from application.database import db

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.sqlite3'
    app.secret_key = 'secret_key'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()
from application.controllers import *

def create_admin():
    admin_exist = User.query.filter_by(email = 'admin@admin.com').first()
    if not admin_exist:
        admin_pwd = 'admin'
        admin_email = 'admin@admin.com'
        user_record = User(email = admin_email, password = admin_pwd, full_name = 'admin', qualification = 'Diploma', dob = '2000-12-12', type = 'admin')
        db.session.add(user_record)
        db.session.commit()
        print('admin created')

with app.app_context():
    db.create_all()
    create_admin()


if __name__ == '__main__':
    app.run(port=5050)