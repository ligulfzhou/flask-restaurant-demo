from flask import jsonify, request, g, current_app, url_for
from .. import db
from . import api
from ..models import Restaurant, User, FoodItem
from .decorators import permission_required


######################################
#
#it is meaningless
#
# @api.route('/foodItems')


@api.route('/foodItems/<int:id>')
def get_foodItems(id):
	foodItem 	= FoodItem.query.filter_by(id=id).first()
	return jsonify(foodItem.to_json())