try:
    from app import db
except ImportError:
    from Lost_And_Found.app import db

class users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    confirmed = db.Column(db.Integer)

    # item=db.relationship('items',backref='users',lazy='dynamic')

    def __init__(self, email, password, confirmed):
        self.email = email
        self.password = password
        self.confirmed = confirmed


class items(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(10000))
    category = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date = db.Column(db.String(255))
    user_id = db.Column(db.Integer)
    image_path = db.Column(db.String(255))

    def __init__(self, name, description, category, location, date, user_id, image_path):
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.date = date
        self.user_id = user_id
        self.image_path = image_path

    def __init__(self, name, description, category, location, date):
        self.name = name
        self.description = description
        self.category = category
        self.location = location
        self.date = date

    def to_json(self):
        item_data = { "name": self.name, "description": self.description, "category": self.category,
                      "location": self.location, "date": self.date }
        return item_data
