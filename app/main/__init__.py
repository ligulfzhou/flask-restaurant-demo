from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission



# then in the html file, we can access the 'permission' -- so-called inject permissions
#  app_context_processor

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
