from flask import Blueprint

api = Blueprint('api', __name__)

from . import authentication, restaurants, users, foodItems, orders
