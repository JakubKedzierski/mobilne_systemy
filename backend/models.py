from app import db
from app import create_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    second_name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    address = db.Column(db.String(500))

    offers = db.relationship("Offer", backref='user', lazy='dynamic')
    contracts = db.relationship("Contract", backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {} {} {}>'.format(self.email, self.first_name, self.second_name)


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255))
    price = db.Column(db.Float)
    publish_date = db.Column(db.Date)
    expiration_date = db.Column(db.Date)
    description = db.Column(db.Text(1000))
    location_latitude = db.Column(db.Date)
    location_longitude = db.Column(db.Date)
    photos = db.Column(db.LargeBinary)
    views = db.Column(db.Integer)
    tags = db.Column(db.Text(2000))

    def __repr__(self):
        return '<Offer {} {} {}>'.format(self.id, self.title, self.price)


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(255))
    tags = db.Column(db.Text(2000))

    def __repr__(self):
        return '<Contract {} {} \ntags:{}>'.format(self.id, self.type, self.tags)