from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, session
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, SearchRestaurantByCity
from .. import db
from ..models import Permission, Role, User, Restaurant, Order, OrderItem, FoodItem
from ..decorators import admin_required, permission_required, staff_required, salesmanager_required



@main.route('/', methods=['GET', 'POST'])
def index():
    '''
        1: when user click search (by city or by restaurant_name),
            --> redirect to result.html

        2:GET
            simply paginate the restaurants
    '''

    page = request.args.get('page', 1, type=int)
    pagination = Restaurant.query.paginate(
        page, per_page=current_app.config['EJILE_RESTAURANT_PER_PAGE'],
        error_out=False)
    restaurants = pagination.items
    return render_template('index.html', restaurants=restaurants, pagination=pagination)



@main.route('/search', methods=['GET','POST'])
def search():
    form = SearchRestaurantByCity()
    if form.validate_on_submit():
        city = form.city.data
        restaurants = Restaurant.query.filter_by(city=city).all()
        return render_template('result.html', restaurants=restaurants)
    return render_template('search.html', form=form)


@main.route('/user/<username>')
def user(username):
    '''
        user homepage

        maybe can dispaly the user`s orders
    '''
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.orders.order_by(Order.timestamp.desc()).paginate(
        page, per_page=current_app.config['EJILE_ORDER_PER_PAGE'],
        error_out=False)
    orders = pagination.items
    return render_template('user.html', user=user, orders=orders,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    '''
        edit profile for user himself
    '''
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.city = form.city.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.city.data = current_user.city
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    '''
        admin can edit everybody's profile 
        admin can also grant staff...and other roles to him
    '''
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.city = form.city.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.city.data = user.city
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/restaurants/<id>')
def restaurants(id):
    restaurant  = Restaurant.query.filter_by(id=id).first()
    fooditems   = restaurant.foodItems
    #fooditems   = FoodItem.query.filter_by(restaurant=restaurant).all()
    return render_template('restaurant.html', restaurant=restaurant, fooditems=fooditems)


@main.route('/fooditems/<id>')
def fooditems(id):
    fooditem    = FoodItem.query.filter_by(id=id).first()
    return render_template('fooditem.html', fooditem=fooditem)


#is the data in session is ill-modifiable ??????
@main.route('/add_to_cart/<int:id>')
@login_required
def add_to_cart(id):
    '''
        use session to hold the fooditems of the cart
    '''
    if 'cart' in session:
        if id in session['cart']:
            session['cart'][id]['count'] += 1
        else:
            fooditem = FoodItem.query.filter_by(id=id).first()
            session['cart'][id] = {}
            session['cart'][id]['name'] = fooditem.name
            session['cart'][id]['price'] = fooditem.price
            session['cart'][id]['count'] = 1
    else:
        session['cart'] = {}
        fooditem = FoodItem.query.filter_by(id=id).first()
        session['cart'][id] = {}
        session['cart'][id]['name'] = fooditem.name
        session['cart'][id]['price'] = fooditem.price
        session['cart'][id]['count'] = 1

    return redirect('/cart')


@main.route('/cart')
@login_required
def cart():
    total_cost = 0
    if 'cart' in session:
        for id in session['cart']:
            total_cost  += session['cart'][id]['price'] * session['cart'][id]['count']

    return render_template("cart.html", cart_items = session['cart'], total = total_cost)



@main.route('/checkout')
@login_required
def checkout():
    #    check whether it is empty
    '''
        this function maybe is the most important function, it build the relationship between the
        tables  -- Orders table, foodItem table, Restaurant table, User table and OrderItem table

        with this function build correctly,
            other operation like restaurant manager confirm the order is received, 
                user confirm received the orderitems of the order......etc
                just to modify the table "ziduan"
                    like : restaurant manager confirm the order is received
                                by make the order "ziduan" done -- from False to True

    '''
    if 'cart' not in session:
        flash('empty cart')
        redirect('.index')
    else:
        total_cost = 0
        res = None
        if 'cart' in session:
            for id in session['cart']:
                if res == None:
                    fooditem = FoodItem.query.filter_by(id=id).first()
                    res = Restaurant.query.filter_by(id=fooditem.restaurant.id).first()

                total_cost  += session['cart'][id]['price'] * session['cart'][id]['count']

        order = Order(user=current_user, total=total_cost, restaurant=res)
        db.session.add(order)

        if 'cart' in session:
            for id in session['cart']:
                fooditem = FoodItem.query.filter_by(id=id).first()
                orderItem = OrderItem(count=session['cart'][id]['count'], \
                            foodItem=fooditem, restaurant=res, order=order)
                db.session.add(orderItem)

    db.session.commit()
    session['cart'] = {}
    return redirect(url_for('main.index'))


@main.route('/request_salesmanager')
@login_required
def request_salesmanager():
    return render_template('request_salesmanager.html')


@main.route('/request_salesmanager/<int:id>')
@login_required
def request_salesmanager_confirmed(id):
    if not current_user.id == id:
        return redirect(url_for('main.index'))
    else:
        role = Role.query.filter_by(name='Salesmanager').first()
        current_user.role = role
        current_user.to_be_confirm_salesmanager = True
        db.session.add(current_user)
        flash('your request for salesmanager role is sent, please wait pationt')
        return redirect(url_for('main.index'))