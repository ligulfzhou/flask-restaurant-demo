from flask import Blueprint

salesmanager = Blueprint('salesmanager', __name__)

from . import views
