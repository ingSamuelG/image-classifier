from wtforms.validators import ValidationError
from . import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.ext.declarative import declarative_base
from . import login_manager

Base = declarative_base()

class Role (db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    slug = db.Column(db.String(64), unique = True)
    users = db.relationship('RateUser', backref='role', lazy= 'dynamic')

    @staticmethod
    def insert_roles():
        Admin = Role(id = 1 , name = "Administrator" ,slug = "super_admin")
        user = Role(id = 2 , name = "User",  slug = "user")

        db.session.add_all([Admin, user])

    def __repr__(self):
        return 'Role %r' % self.name

class RateUser (UserMixin, db.Model):
    __tablename__='rate_users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id= db.Column(db.Integer , db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default = False)
    first_name= db.Column(db.String(64))
    last_name= db.Column(db.String(64))
    organization= db.Column(db.String(64))
    change_code_hash = db.Column(db.String(128))
    change_code_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return 'User %r' % self.first_name
    
    @staticmethod
    def add_test_user():
        user = RateUser(email  = "test_user@test.com", first_name = "Test" , last_name = "User", password = "test1234", organization = "Test user created in shell", role_id = 2)
        db.session.add(user)


    @staticmethod
    def add_user(email, first, lastname, password):
        user = RateUser(email  = email, first_name = first , last_name = lastname, password = password, organization = "Test user created in shell", role_id = 2)
        db.session.add(user)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @property
    def change_code(self):
        raise AttributeError('the reset code is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    @change_code.setter
    def change_code(self,code):
        self.change_code_hash = generate_password_hash(code)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def verify_code(self, code):
        return check_password_hash(self.change_code_hash, code)
    
    def to_json(self):
        json_user = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'confirmed': self.confirmed,
            'role': self.role_id,
            'created_at': self.created_at,
            }
        return json_user
    
    
    @login_manager.user_loader
    def load_user(user_id):
        return RateUser.query.get(int(user_id))

class Image(db.Model):
    __tablename__='images'
    id =  db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    url =  db.Column(db.String(255))
    title = db.Column(db.String(255))
    tags = db.Column(db.String(255))
    num_ratings =  db.Column(db.Integer)
    total_rating =  db.Column(db.Integer)
    views =  db.Column(db.Integer)
    width =  db.Column(db.Integer)
    height =  db.Column(db.Integer)
    source = db.Column(db.String(255))
    image_set_id =  db.Column(db.Integer)
    created_at =  db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    thumb_url = db.Column(db.String(255))
    flag =  db.Column(db.Integer)
    image_file_path =  db.Column(db.String(255))
    thumb_file_path =  db.Column(db.String(255))
    xh_views = db.Column(db.Integer)
    xh_total_rating =  db.Column(db.Integer)
    ratio =  db.Column(db.Integer)
    image_label_rating = db.relationship('Image_label', backref='image', cascade = "all,delete, delete-orphan", lazy='dynamic')

class Image_label(db.Model):
    __tablename__='image_labels'
    id = db.Column(db.Integer, primary_key=True)
    images_id= db.Column(db.Integer , db.ForeignKey('images.id'))
    rating = db.Column(db.Integer)
