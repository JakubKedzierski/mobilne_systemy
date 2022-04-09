from .app import db, create_app
from .user_errors import ValueNotSet
from datetime import date
import json
from dateutil import parser
from werkzeug.security import generate_password_hash

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    second_name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(500), nullable=False)

    offers = db.relationship("Offer", backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {} {} {}>'.format(self.email, self.first_name, self.second_name)


    def from_dict(self, data):
        fields = ['firstName', 'secondName', 'email', 'password', 'phone', 'address']
        for field in fields:
            if field not in data:
                raise ValueNotSet("Field: "+ field + " not present in json")

        self.first_name = data['firstName']
        self.second_name = data['secondName']
        self.email = data['email']

        # validate password
        self.password = generate_password_hash(data['password'], method='sha256') 
        self.phone = data['phone']
        self.address = data['address']


    def to_dict(self):
        return_dict = {
            "firstName" : self.first_name,
            "secondName" : self.second_name,
            "email" : self.email,
            "phone" : self.phone,
            "address" : self.address
        }

        return return_dict


class Offer(db.Model):
    __tablename__ = 'offer'

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

    contracts = db.relationship("Contract", backref='offer', lazy='dynamic')

    def __repr__(self):
        return '<Offer {} {} {}>'.format(self.id, self.title, self.price)

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
        if serialized_photos is not None:
            self.photos = serialized_photos
        else:
            self.photos = ''

        serialized_tags = json.dumps(data['tags'])
        if serialized_tags is not None:
            self.tags = serialized_tags 
        else:
            self.tags = ''      
        
        self.publish_date = date.today()
        self.views = 0

    def to_dict(self):
        return_dict = {
            "offerId" : self.id,
            "user" : self.user.to_dict(),
            "name" : self.name,
            "price" : self.price,
            "publishDate" : self.publish_date.isoformat(),
            "description" : self.description,
            "location" : {
                "latitude" : self.location_latitude,
                "longitude" : self.location_longitude
            },
            "photos" : json.loads(self.photos),
            "views" : self.views,
            "tags" : json.loads(self.tags)
        }

        return return_dict


class Contract(db.Model):
    __tablename__ = 'contract'

    id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'))
    type = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.Text(2000))

    def __repr__(self):
        return '<Contract {} {} \ntags:{}>'.format(self.id, self.type, self.tags)

    def from_dict(self, data):
        fields = ['offerId', 'contract']
        for field in fields:
            if field not in data:
                raise ValueNotSet("Field: "+ field + " not present in json")

        fields = ['type', 'tags']
        for field in fields:
            if field not in data['contract']:
                raise ValueNotSet("Field: "+ field + " not present in json")
        
        self.offer_id = data['offerId']
        self.type = data['contract']['type']
        
        serialized_tags = json.dumps(data['contract']['tags'])
        if serialized_tags is not None:
            self.tags = serialized_tags
        else:
            self.tags = ''  
