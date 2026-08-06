from flask import Blueprint
from db import get_connection

admin = Blueprint("admin", __name__)
