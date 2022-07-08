from flask import Blueprint

classifier = Blueprint('classifier', __name__)

from . import views