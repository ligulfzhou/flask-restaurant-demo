from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import Restaurant, User, FoodItem, OrderItem
from .decorators import permission_required

@api.route('/orderItems/<int:id>')
def get_orderItems(id):
	orderItem 	= OrderItem.query.get_or_404(id)
	return jsonify(orderItem.to_json())
