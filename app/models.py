from . import db

class Role(db.Model):
    __tablename__   = 'roles'
    id              = db.Column(db.Integer, primary_key = True)
    name            = db.Column(db.string(64), unique = True)
    users           = db.relationship('User', backref = 'role', lazy = 'dynamic')


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