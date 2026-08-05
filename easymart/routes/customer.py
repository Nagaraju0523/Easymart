from flask import Blueprint, render_template, request
from db import get_connection

customer = Blueprint("customer", __name__)

@customer.route("/register", methods=["GET", "POST"])
def register():


    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["PhoneNumber"]
        password = request.form["password"]
        address = request.form["address"]
        

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Customers
            (Name, Email, PhoneNumber, Password, Address)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, password, address))

        conn.commit()

        cursor.close()
        conn.close()

        return render_template("customer/success.html")

    return render_template("customer/register.html")


@customer.route("/login", methods=["GET"])
def login():
    return render_template("customer/login.html")