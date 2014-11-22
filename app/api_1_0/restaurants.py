from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import Restaurant, User, FoodItem, OrderItem, Order, OrderItem
from .decorators import permission_required

@api.route('/restaurants/')
def get_restaurants():
	page = request.args.get('page', 1, type=int)
	pagination = Restaurant.query.paginate(
		page, per_page=current_app.config['EJILE_RESTAURANT_PER_PAGE'],
		error_out=False)
	restaurants = pagination.items

	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_restaurants', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_restaurants', page=page+1, _external=True)
	return jsonify({
		'restaurants' : [restaurant.to_json() for restaurant in restaurants],
		'prev' : prev,
		'next' : next,
		'count' : pagination.total
		})


@api.route('/restaurants/<int:id>')
def get_restaurant(id):
	restaurant = Restaurant.query.get_or_404(id)
	return jsonify(restaurant.to_json())


@api.route('/restaurants/<int:id>/foodItems')
def get_restaurant_foodItems(id):
	restaurant 	= Restaurant.query.get_or_404(id)
	#foodItems 	= restaurant.foodItems
	foodItems 	= FoodItem.query.filter_by(restaurant_id=id).all()
	return jsonify({
			'foodItems' : [foodItem.to_json() for foodItem in foodItems]
		})


@api.route('/restaurants/<int:id>/orderItems')
def get_restaurant_orderItems(id):
	restaurant 	= Restaurant.query.get_or_404(id)
	orderItems 	= restaurant.orderItems
	#orderItems 	= OrderItem.query.filter_by(restaurant_id=id).all()
	return jsonify({
			'orderItems' : [orderItem.to_json() for orderItem in orderItems]
		})


@api.route('/restaurants/<int:id>/orders')
def get_restaurant_orders(id):
	restaurant 	= Restaurant.query.get_or_404(id)
	#orders 		= restaurant.orders
	orders 		= Order.query.filter_by(restaurant_id=id).all()
	return jsonify({
			'orders' : [order.to_json() for order in orders]
		})

