from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import Restaurant, User, Order, Permission, OrderItem
from .decorators import permission_required



@api.route('/orders/<int:id>')
def get_order(id):
	order = Order.query.get_or_404(id)
	return jsonify(order.to_json())



@api.route('/orders/<int:id>/orderitems')
def get_order_orderItems(id):
	order 		= Order.query.get_or_404(id)
	orderItems 	= order.orderItems
	#orderItems 	= OrderItem.query.filter_by(order=order).all()
	return jsonify({
			'orderItems' : [orderItem.to_json() for orderItem in orderItems]
		})


#
#---post methods: so users can make orders
#

#make order must least have the usual permission
#actually, all kinds of users has the usual permission

@api.route('/orders', methods=['POST'])
@permission_required(Permission.USUAL)
def new_order():
	order = Order.from_json(request.json)
	order.customer = g.current_user
	db.session.add(order)
	db.session.commit()
	return jsonify(order.to_json()), 201, \
        {'Location': url_for('api.get_order', id=order.id, _external=True)}
