from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from app.exceptions import ValidationError
from . import db, login_manager


class Permission:
    USUAL = 0x01
    SALESMANAGER = 0x03
    STAFF = 0x04
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.USUAL, True),
            'Salesmanager': (Permission.USUAL |
                          Permission.SALESMANAGER, False),
            'Staff': (Permission.USUAL |
                        Permission.STAFF, False),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id                          = db.Column(db.Integer, primary_key=True)
    email                       = db.Column(db.String(64), unique=True, index=True)
    username                    = db.Column(db.String(64), unique=True, index=True)
    password_hash               = db.Column(db.String(128))
    confirmed                   = db.Column(db.Boolean, default=False)
    name                        = db.Column(db.String(64))
    city                        = db.Column(db.String(64)) 
    about_me                    = db.Column(db.Text())
    member_since                = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen                   = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash                 = db.Column(db.String(32))

    to_be_confirm_salesmanager  = db.Column(db.Boolean, default=False)
    
    role_id                     = db.Column(db.Integer, db.ForeignKey('roles.id'))
    orders                      = db.relationship('Order', backref = 'user', lazy = 'dynamic')
    restaurants                 = db.relationship('Restaurant', backref='user', lazy = 'dynamic')

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     city=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['EJILE_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                ''' initial the user with default permission'''
                self.role = Role.query.filter_by(default=True).first() 
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def is_salesmanager(self):
        return self.can(Permission.SALESMANAGER)  and  not self.can(Permission.ADMINISTER)


    #is_staff --> we allow   both  staff and administrator
    def is_staff(self):
        #return self.can(Permission.STAFF) and not self.can(dPermission.ADMINISTER)
        return self.can(Permission.STAFF)

    def is_user(self):
        return self.can(Permission.USUAL) and not self.can(Permission.ADMINISTER) \
                and not self.can(Permission.STAFF) and not self.can(Permission.SALESMANAGER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def gravatar(self, size=100, default='identicon', rating='g'):
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)



    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'orders': url_for('api.get_user_orders', id=self.id, _external=True),
        }
        return json_user


    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return '<User %r>' % self.username


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def is_manager(self):
        return False

    def is_staff(self):
        return False


login_manager.anonymous_user = AnonymousUser



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class Order(db.Model):
    __tablename__   = 'orders'
    id              = db.Column(db.Integer, primary_key = True)
    total           = db.Column(db.Float)
    timestamp       = db.Column(db.DateTime, default=datetime.utcnow)

    #users make order, waiting for the salesmanager to confirm
    done            = db.Column(db.Boolean, default=False)

    orderItems      = db.relationship('OrderItem', backref = 'order', lazy = 'dynamic')
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    restaurant_id   = db.Column(db.Integer, db.ForeignKey('restaurants.id'))


    def to_json(self):
        json_order = {
            'url' : url_for('api.get_order', id=self.id, _external=True),
            'total' : self.total,
            'timestamp' : self.timestamp,
            'done' : self.done,
            'orderItems' : url_for('api.get_order_orderItems', id=self.id, _external=True),
            'user' : url_for('api.get_user', id=self.user_id, external=True),
            'restaurant' : url_for('api.get_restaurant', id=self.restaurant_id,external=True)
        }
        return json_order

    def from_json(json_order):
        total = json_order.get('total')
        orderItems = json_order.get('orderItems')
        user_id = json_order.get('user_id')
        restaurant_id = json_order.get('restaurant_id')
        return Order(total=total, orderItems=orderUtems,user_id=user_id,\
                restaurant_id=restaurant_id)


class OrderItem(db.Model):
    __tablename__   = 'orderItems'
    id              = db.Column(db.Integer, primary_key = True)
    count           = db.Column(db.Integer)

    foodItem_id     = db.Column(db.Integer, db.ForeignKey('foodItems.id'))
    restaurant_id   = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    order_id        = db.Column(db.Integer, db.ForeignKey('orders.id'))

    def to_json(self):
        json_orderitem = {
            'url' : url_for('api.get_orderItems', id=self.id, _external=True),
            'count' : self.count,
            'restaurant_id' : url_for('api.get_restaurant', id=self.restaurant_id, _external=True),
            'foodItem_id' : url_for('api.get_foodItems', id=self.foodItem_id, _external=True),
            'order_id' : url_for('api.get_order', id=self.order_id, _external=True)
        }
        return json_orderitem

    def from_json(json_orderitem):
        count = json_orderitem.get('count'),
        restaurant_id = json_orderitem.get('restaurant_id')
        foodItem_id = json_orderitem.get('foodItem_id')

        return OrderItem(count=count,restaurant_id=restaurant_id,foodItem_id=foodItem_id)


class FoodItem(db.Model):
    __tablename__   = 'foodItems'
    id              = db.Column(db.Integer, primary_key = True) 
    price           = db.Column(db.Float)
    imageurl        = db.Column(db.Text)
    name            = db.Column(db.String(64))
    description      = db.Column(db.Text)

    orderItems      = db.relationship('OrderItem', backref = 'foodItem', lazy = 'dynamic')
    restaurant_id   = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    def to_json(self):
        json_foodItem = {
            'url' : url_for('api.get_foodItems', id=self.id, _external=True),
            'price' : self.price,
            'imageurl' : self.imageurl,
            'name' : self.name,
            'description' : self.description
        }
        return json_foodItem

class Restaurant(db.Model):
    __tablename__   = 'restaurants'
    id              = db.Column(db.Integer, primary_key = True)
    name            = db.Column(db.String(64))
    city            = db.Column(db.String(64))
    description     = db.Column(db.Text)
    imageurl        = db.Column(db.Text)

    foodItems       = db.relationship('FoodItem', backref = 'restaurant', lazy = 'dymamic')
    orderItems      = db.relationship('OrderItem', backref = 'restaurant', lazy = 'dynamic')
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'))
    orders          = db.relationship('Order', backref='restaurant', lazy='dynamic')

    def to_json(self):
        json_restaurant = {
            'url' : url_for('api.get_restaurant', id=self.id, _external=True),
            'name' : self.name,
            'city' : self.city,
            'description' : self.description,
            'imageurl' : self.imageurl,
            'foodItems' : url_for('api.get_restaurant_foodItems', id=self.id, _external=True),
            'orderItems' : url_for('api.get_restaurant_orderItems', id=self.id, _external=True),
            'user_id' : url_for('api.get_user', id=self.user_id, _external=True),
            'orders' : url_for('api.get_restaurant_orders', id=self.id, _external=True)
        }
        return json_restaurant
