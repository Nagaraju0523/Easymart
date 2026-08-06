from flask import Blueprint, render_template, request, session, redirect
from db import get_connection

customer = Blueprint("customer", __name__)

# ---------------- Customer Registration ----------------
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

        try:
            cursor.execute("""
                INSERT INTO Customers
                (Name, Email, PhoneNumber, Password, Address)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, phone, password, address))

            conn.commit()

            return render_template("customer/success.html")

        except Exception as e:
            return f"Error: {e}"

        finally:
            cursor.close()
            conn.close()

    return render_template("customer/register.html")


# ---------------- Customer Login ----------------
@customer.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT CustomerId, Name
            FROM Customers
            WHERE Email=%s AND Password=%s
        """, (email, password))

        user = cursor.fetchone()

        print("User:", user)

        cursor.close()
        conn.close()

        if user:
            session["customer_id"] = user[0]
            session["customer_name"] = user[1]

            return redirect("/dashboard")

        return "Invalid Email or Password"

    return render_template("customer/login.html")


# ---------------- Customer Dashboard ----------------
@customer.route("/dashboard")
def dashboard():

    if "customer_id" not in session:
        return redirect("/login")

    return render_template(
        "customer/dashboard.html",
        name=session["customer_name"]
    )


# ---------------- Customer Logout ----------------
@customer.route("/logout")
def logout():

    session.clear()

    return redirect("/login")