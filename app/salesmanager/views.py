from flask import render_template, redirect, url_for, abort, flash, request, \
                   current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import salesmanager

from .. import db
from ..models import Permission, Role, User, Order, OrderItem, Restaurant, FoodItem
from ..decorators import admin_required, staff_required, salesmanager_required


#using next_id to change the image name
def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


@salesmanager.route('/')
@login_required
@salesmanager_required
def index():
    
    ''' in this page put whatever something '''
    '''
        maybe to put some links
        1: --> manage restaurants
        2: --> manage unhandled orders
    '''
    
    return render_template('/salesmanager/index.html')



@salesmanager.route('/salesrestaurants')
@login_required
@salesmanager_required
def salesrestaurants():

    restaurants = current_user.restaurants
    return render_template('/salesmanager/restaurants.html', restaurants=restaurants)



@salesmanager.route('/salesrestaurants/<id>')
@login_required
@salesmanager_required
def salesrestaurant(id):
    
    ''' this restaurant page to handle fooditem upload'''

    restaurant      = Restaurant.query.filter_by(id=id).first()
    fooditems       = restaurant.foodItems
    
    return render_template('/salesmanager/restaurant.html', restaurant=restaurant, fooditems=fooditems)



@salesmanager.route('/unhandledorders')
@salesmanager_required
@login_required
def unhandled_orders():
    '''
        a list of orders ..... 
        every order add a link, to trigger a /handle_order/<orderid>/done
    '''
    
    return 



@salesmanager.route('/handle/<orderid>/done')
@salesmanager_required
@login_required
def handle_order(orderid):
    order       = Order.query.filter_by(id=orderid).first()
    order.done  = True
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('salesmanager.unhandledorders'))



@salesmanager.route('/fooditem/<id>/delete')
@salesmanager_required
@login_required
def deletefood(id):
    fooditem    = FoodItem.query.filter_by(id=id).first()
    db.session.delete(fooditem)
    db.session.commit()
    return redirect(url_for('salesmanager.salesrestaurants'))



@salesmanager.route('/fooditem/<id>/alter')
@login_required
@salesmanager_required
def alterfood(id):
    fooditem    = FoodItem.query.filter_by(id=id).first()
