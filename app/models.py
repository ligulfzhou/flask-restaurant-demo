from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_user, request
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager


class Permission:
    FOLLOW              = 0x01
    COMMENT             = 0x02
    WRITE_ARTICLE       = 0x04
    MODERATE_COMMENTS   = 0x08
    ADMINISTER          = 0x80


class Role(db.Model):
    __tablename__   = 'roles'
    id              = db.Column(db.Integer, primary_key = True)
    name            = db.Column(db.string(64), unique = True)
    default         = db.Column(db.Boolean, default=False, index=True)
    permisions      = db.Column(db.Integer)
    users           = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User' : (Permission.FOLLOW |
                        Permission.COMMENT | 
                        Permission.WRITE_ARTICLE, True),
            'Moderator' : (Permission.FOLLOW |
                            Permission.COMMENT |
                            Permission.WRITE_ARTICLE|
                            Permission.MODERATE_COMMENTS, False),
            'Administrator' : (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                


class User(db.Model):
    __tablename__   = 'users'
    id              = db.Column(db.Integer, primary_key = True)
    username        = db.Column(db.string(64), unique = True)
    role_id         = db.Column(db.Integer, db.ForeignKey('role.id'))
    orders          = db.relationship('Order', backref = 'user', lazy = 'dynamic')


class Order(db.Model):
    __tablename__   = 'orders'
    id              = db.Column(db.Integer, primary_key = True)
    total           = db.Column(db.Float)
    address         = db.Column(db.Text)
    orderItems      = db.relationship('OrderItem', backref = 'order')
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'), lazy = 'dynamic')

class OderItem(db.Model):
    __tablename__   = 'orderItems'
    id              = db.Column(db.Integer, primary_key = True)
    restaurant_id   = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    order_id        = db.Column(db.Integer, db.ForeignKey('orders.id'))
    count           = db.Column(db.Integer)

class FoodItem(db.Model):
    __tablename__   = 'foodItems'
    id              = db.Column(db.Integer, primary_key = True)
    restaurant_id   = db.Column(db.Integer, db.ForeignKey('restaurant.id')) 
    price           = db.Column(db.Float, required = True) #--------------------
    image           = db.Column(db.Text)
    name            = db.Column(db.String(64))
    descrption      = db.Column(db.Text)

class Restaurant(db.Model):
    __tablename__   = 'restaurants'
    id              = db.Column(db.Integer, primary_key = True)
    name            = db.Column(db.String(64))
    foodItems       = db.relationship('FoodItem', backref = 'restaurant', lazy = 'dymamic')
    orderItems      = db.relationship('OrderItem', backref = 'restaurant', lazy = 'dynamic')
    province        = db.Column(db.String(64))
    city            = db.Column(db.String(64))
    district        = db.Column(db.String(64))
    description     = db.Column(db.Text)