from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://pzzefhssgkjmcx:jCBwCVMY6h14IJrvXRGwBWnOzp@ec2-107-21-101-67.compute-1.amazonaws.com:5432/darmgk9hj6s40v'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db = SQLAlchemy(app)

class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    lastname = db.Column(db.String(120))
    firstname = db.Column(db.String(120))
    Idnumber= db.Column(db.String(120), unique=True)
    gender = db.Column(db.String(120))
    age= db.Column(db.String(120))
    date = db.Column(db.String(120))
    image=db.Column(db.String(120))

    def __init__(self, username, lastname,firstname,Idnumber,gender,age,date,image):
        self.username = username
        self.lastname=lastname
        self.firstname=firstname
        self.Idnumber=Idnumber
        self.gender=gender
        self.age=age
        self.date=date
        self.image=image
    def __repr__(self):
        return '<User %r>' % self.username



