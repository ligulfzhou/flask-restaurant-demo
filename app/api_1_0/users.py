from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Order


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/orders')
def get_user_orders(id):
	user = User.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	pagination = user.orders.order_by(Order.timestamp.desc()).paginate(
		page, per_page=current_app.config['EJILE_ORDER_PER_PAGE'],
		error_out=False)
	orders = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_user_orders', page=page-1, _external=True)
	next = None
	if pagination.has_prev:
		next = url_for('api.get_user_orders', page=page+1, _external=True)
	return jsonify({
		'order' : [order.to_json() for order in orders],
		'prev' : prev,
		'next' : next,
		'count' : pagination.total
		})