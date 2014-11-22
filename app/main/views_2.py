from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, SearchRestaurantOrCity
from .. import db
from ..models import Permission, Role, User, Restaurant, Order, OrderItem, FoodItem
from ..decorators import admin_required, permission_required, staff_required, salesmanager_required


#maybe i should seperate the search page and the index page
#
#
#


#or maybe i must turn to the js for help

@main.route('/', methods=['GET', 'POST'])
def index():
    '''
        1: when user click search (by city or by restaurant_name),
            --> redirect to result.html

        2:GET
            simply paginate the restaurants
    '''
    form = SearchRestaurantOrCity()
    if form.validate_on_submit():
        cityorname_data = form.cityorresname.data
        cityorname = form.radiobutton.data
        if cityorname == 1:
            restaurants = Restaurant.query.filter_by(city=cityorname_data).all()
        else:
            restaurants = Restaurant.query.filter_by(name=cityorname).all()
        return render_template('result.html', restaurants=restaurants)
        


        #------------------------------------------------------------------------------

        #return redirect(url_for('.result'))


        #--------------------------------------------------------------------------------
    page = request.args.get('page', 1, type=int)
    pagination = Restaurant.query.paginate(
        page, per_page=current_app.config['EJILE_RESTAURANT_PER_PAGE'],
        error_out=False)
    restaurants = pagination.items
    return render_template('index.html', form=form, restaurants=restaurants, pagination=pagination)



#-----------------------------------------------------------
@main.route('/result')
def result():
    return render_template('result.html')
#-----------------------------------------------------------



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
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    '''
        admin can edit everybody`s profile 
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
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/restaurants/<id>')
def restaurant(id):
    restaurant  = Restaurant.query.filter_by(id=id).first()
    fooditems   = restaurant.fooditems
    return render_template('restaurant.html', restaurant=restaurant, fooditems=fooditems)

@main.route('/fooditem/<id>')
def fooditem(id):
    fooditem    = FoodItem.query.filter_by(id=id).first()
    render_template('fooditem.html', fooditem=fooditem)
