from flask import render_template, redirect, url_for, abort, flash, request, \
                   current_app, make_response
from flask.ext.login import login_required, current_user
from flask.ext.sqlalchemy import get_debug_queries
from . import admin

from .. import db
from ..models import Permission, Role, User, Order, OrderItem, Restaurant, FoodItem
from ..decorators import admin_required, staff_required, salesmanager_required



#	'''
#										           / salesmanager 
#										          /
#		staff/admin can enable and disable user
#										          \
#										           \ user(normal)
#
#
#   the grant permission is admin only ---- (implemented in the main directory /edit-profile/<id> )	
#'''

@admin.route('/')
@login_required
@staff_required
def index():
	return render_template('/admin/index.html')