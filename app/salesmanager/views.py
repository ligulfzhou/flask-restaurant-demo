from flask import render_template, redirect, url_for, abort, flash, request, \
                   current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import salesmanager
from .forms import RestaurantForm, FoodItemForm

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



@salesmanager.route('/salesrestaurants', methods=['GET','POST'])
@login_required
@salesmanager_required
def salesrestaurants():

    form = RestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(name = form.name.data,
                                city = form.city.data,
                                description = form.description.data,
                                user = current_user
            )
        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for('salesmanager.salesrestaurants'))

    restaurants = current_user.restaurants
    return render_template('/salesmanager/restaurants.html', restaurants=restaurants, form=form)



@salesmanager.route('/salesrestaurants/<int:id>', methods=['GET','POST'])
@login_required
@salesmanager_required
def salesrestaurant(id):
    
    ''' this restaurant page to handle fooditem upload'''
    form = FoodItemForm()

    restaurant      = Restaurant.query.get_or_404(id)
    fooditems       = restaurant.foodItems

    if form.validate_on_submit():
        foodItem    = FoodItem(price = form.price.data,
                                name = form.name.data,
                                description = form.description.data,
                                restaurant = restaurant
            )
        db.session.add(foodItem)
        db.session.commit()
        return redirect(url_for('salesmanager.salesrestaurant', id=id))
        

    
    return render_template('/salesmanager/restaurant.html', restaurant=restaurant, fooditems=fooditems, form=form)



@salesmanager.route('/unhandledorders')
@salesmanager_required
@login_required
def unhandled_orders():
    '''
        a list of orders ..... 
        every order add a link, to trigger a /handle_order/<orderid>/done
    '''
    
    return 


#---------------check order is made by user-----------------
# only make the order table` ZIDUAN done to True-------------
@salesmanager.route('/handle/<orderid>/done')
@salesmanager_required
@login_required
def handle_order(orderid):
    order       = Order.query.filter_by(id=orderid).first()
    order.done  = True
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('salesmanager.unhandledorders'))


#---------------delete restaurant---------------------
@salesmanager.route('salesrestaurants/<int:id>/delete')
@salesmanager_required
@login_required
def delete_restaurant(id):
    restaurant  = Restaurant.query.get_or_404(id)
    if current_user != restaurant.user:
        return redirect(url_for('main.index'))
    db.session.delete(restaurant)
    db.session.commit()
    return redirect(url_for('salesmanager.salesrestaurants'))



#-----------alter restaurant information------------------
@salesmanager.route('salesrestaurants/<int:id>/alter', methods=['GET','POST'])
@salesmanager_required
@login_required
def alter_restaurant(id):

    form = RestaurantForm()

    restaurant  = Restaurant.query.get_or_404(id)
    if current_user != restaurant.user:
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        restaurant.name         = form.name.data
        restaurant.description  = form.description.data
        restaurant.city         = form.city.data

        db.session.add(restaurant)
        flash('you alter your restaurant information')
        return redirect(url_for('salesmanager.salesrestaurants'))
    form.name.data          = restaurant.name
    form.description.data   = restaurant.description
    form.city.data          = restaurant.city
    return render_template('salesmanager/alter_restaurant.html', form=form)



#----------------delete fooditem---------------------------
@salesmanager.route('/fooditem/<id>/delete')
@salesmanager_required
@login_required
def delete_fooditem(id):
    fooditem    = FoodItem.query.get_or_404(id)
    if fooditem.restaurant.user != current_user:
        flash('you do not have the permission -- for the fooditem is not your restaurant`s ')
        return redirect(url_for('main.index'))
    db.session.delete(fooditem)
    db.session.commit()
    return redirect(url_for('salesmanager.salesrestaurant', id=fooditem.restaurant.id))



#---------------alter fooditem-------------------------------
@salesmanager.route('/fooditem/<id>/alter', methods=['GET','POST'])
@login_required
@salesmanager_required
def alter_fooditem(id):

    form = FoodItemForm()

    fooditem    = FoodItem.query.get_or_404(id)
    if fooditem.restaurant.user != current_user:
        flash('you do not have the permission -- for the fooditem is not your restaurant`s')
        return redirect(url_for('main.index'))

    if form.validate_on_submit():
        fooditem.price          = form.price.data
        fooditem.name           = form.name.data
        fooditem.description    = form.description.data

        db.session.add(fooditem)
        flash('you alter your fooditem successfully')
        return redirect(url_for('salesmanager.salesrestaurant', id=fooditem.restaurant.id))
    form.name.data          = fooditem.name
    form.price.data         = fooditem.price
    form.description.data   = fooditem.description
    return render_template('salesmanager/alter_fooditem.html', form=form)



@salesmanager.route('/ungranted')
@login_required
@salesmanager_required
def ungranted():
    if current_user.to_be_confirm_salesmanager == False:
        return redirect(url_for('main.index'))
    return render_template('salesmanager/ungranted.html')
