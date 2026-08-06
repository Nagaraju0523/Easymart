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

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ProductId,
               ProductName,
               Category,
               Price,
               Quantity,
               Description,
               Image
        FROM Products
    """)

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "customer/dashboard.html",
        name=session["customer_name"],
        products=products
    )

# ---------------- Add to Cart ----------------
@customer.route("/add-cart/<int:product_id>", methods=["POST"])
def add_cart(product_id):

    if "customer_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the product is already in the cart
    cursor.execute("""
        SELECT CartId, Quantity
        FROM Cart
        WHERE CustomerId=%s AND ProductId=%s
    """, (session["customer_id"], product_id))

    item = cursor.fetchone()

    if item:
        # Increase quantity if already in cart
        cursor.execute("""
            UPDATE Cart
            SET Quantity = Quantity + 1
            WHERE CartId=%s
        """, (item[0],))
    else:
        # Add new product to cart
        cursor.execute("""
            INSERT INTO Cart (CustomerId, ProductId, Quantity)
            VALUES (%s, %s, %s)
        """, (
            session["customer_id"],
            product_id,
            1
        ))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/dashboard") 

# ---------------- My Cart ----------------
@customer.route("/cart")
def cart():

    if "customer_id" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            Cart.ProductId,
            Products.ProductName,
            Products.Price,
            Cart.Quantity,
            Products.Image
        FROM Cart
        JOIN Products
        ON Cart.ProductId = Products.ProductId
        WHERE Cart.CustomerId = %s
    """, (session["customer_id"],))

    cart = cursor.fetchall()

    total = 0

    for item in cart:
        total += item[2] * item[3]

    cursor.close()
    conn.close()

    return render_template(
        "customer/cart.html",
        cart=cart,
        total=total
    )

# ---------------- Customer Logout ----------------
@customer.route("/logout")
def logout():

    session.clear()

    return redirect("/login")