from .app import db
from .app import create_app
from .user_errors import ValueNotSet
from datetime import date
import json
from dateutil import parser

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    second_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(500), nullable=False)

    offers = db.relationship("Offer", backref='user', lazy='dynamic')
    contracts = db.relationship("Contract", backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {} {} {}>'.format(self.email, self.first_name, self.second_name)


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    publish_date = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    location_latitude = db.Column(db.Float, nullable=False)
    location_longitude = db.Column(db.Float, nullable=False)
    photos = db.Column(db.Text)
    views = db.Column(db.Integer)
    tags = db.Column(db.Text)

    def __repr__(self):
        return '<Offer {} {} {}>'.format(self.id, self.title, self.price)

    def to_dict(self):
        deserialized_photos = json.loads(self.photos)

    def from_dict(self, data):
        fields = ['name', 'price','expirationDate', 'description', 'location', 'photos', 'tags']
        for field in fields:
            if field not in data:
                raise ValueNotSet("Field: "+ field + " not present in json")
        
        locations = ['latitude', 'longitude']
        for location_field in locations:
            if location_field not in data['location']:
                raise ValueNotSet("Field: "+ location_field + " not present in json")
        
        self.name = data['name']
        self.price = data['price']
        self.expiration_date = parser.parse(data['expirationDate'])
        self.description = data['description']
        self.location_latitude = data['location']['latitude']
        self.location_longitude = data['location']['longitude']
        
        serialized_photos = json.dumps(data['photos'])
        self.photos = serialized_photos
        self.tags = json.dumps(data['tags'])        
        
        self.publish_date = date.today()
        self.views = 0


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    type = db.Column(db.String(255), nullable=False)
    tags = db.Column(db.Text(2000))

    def __repr__(self):
        return '<Contract {} {} \ntags:{}>'.format(self.id, self.type, self.tags)