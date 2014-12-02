from flask import render_template, redirect, url_for, abort, flash, request, \
                   current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import admin
from .forms import EditProfileAdminForm

from .. import db
from ..models import Permission, Role, User, Order, OrderItem, Restaurant, FoodItem
from ..decorators import admin_required, staff_required, salesmanager_required


#										           / salesmanager 
#										          /
#		staff/admin can enable and disable user
#										          \
#										           \ user(normal)
#
#   the grant permission is admin only ---- (implemented in the main directory /edit-profile/<id> )	


@admin.route('/')
@login_required
@staff_required
def index():
	return render_template('/admin/index.html')


@admin.route('/edit_users_profile')
@login_required
@admin_required
def edit_users_profile():
	users	= User.query.all()
	return render_template('/admin/edit_users_profile.html', users=users)


@admin.route('/handle_salesmanager_request')
@login_required
@staff_required
def handle_salesmanager_request():
    salesmanager_role = Role.query.filter_by(name='Salesmanager').first()
    request_users = User.query.filter_by(to_be_confirm_salesmanager=True).filter_by(role=salesmanager_role).all()
    return render_template('admin/handle_salesmanager_request.html', users=request_users)

@admin.route('/grant_salesmanager_request/<int:id>')
@admin_required
@login_required
def grant_salesmanager_request(id):
    user = User.query.filter_by(id=id).first()
    user.to_be_confirm_salesmanager = False
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('admin.handle_salesmanager_request'))


@admin.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
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

