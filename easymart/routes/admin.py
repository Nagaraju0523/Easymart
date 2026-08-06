from flask import Blueprint
from db import get_connection

Admin = Blueprint("admin", __name__)
