from flask import Blueprint, render_template, request, redirect, session
from werkzeug.utils import secure_filename
from db import get_connection
import os

seller = Blueprint("seller", __name__)
UPLOAD_FOLDER = "static/uploads"

# ---------------- Seller Registration ----------------
@seller.route("/seller/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        shop_name = request.form["shop_name"]
        owner_name = request.form["owner_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        address = request.form["address"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Sellers
            (ShopName, OwnerName, Email, PhoneNumber, Password, Address)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            shop_name,
            owner_name,
            email,
            phone,
            password,
            address
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/seller/login")

    return render_template("seller/register.html")
# ---------------- Seller Login ----------------
@seller.route("/seller/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SellerId, OwnerName
            FROM Sellers
            WHERE Email=%s AND Password=%s
        """, (email, password))

        seller_data = cursor.fetchone()

        cursor.close()
        conn.close()

        if seller_data:
            session["seller_id"] = seller_data[0]
            session["seller_name"] = seller_data[1]

            return redirect("/seller/dashboard")

        return "Invalid Email or Password"

    return render_template("seller/login.html")
# ---------------- Seller Dashboard ----------------
@seller.route("/seller/dashboard")
def dashboard():

    if "seller_id" not in session:
        return redirect("/seller/login")

    return render_template(
        "seller/dashboard.html",
        seller_name=session["seller_name"]
    )

# ---------------- Add Product ----------------
@seller.route("/seller/add-product", methods=["GET", "POST"])
def add_product():

    # Seller must be logged in
    if "seller_id" not in session:
        return redirect("/seller/login")

    if request.method == "POST":

        product_name = request.form["product_name"]
        category = request.form["category"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        description = request.form["description"]

        image = request.files["image"]

        filename = secure_filename(image.filename) 

        image.save(os.path.join(UPLOAD_FOLDER, filename))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Products
            (SellerId, ProductName, Category, Price, Quantity, Description, Image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            session["seller_id"],
            product_name,
            category,
            price,
            quantity,
            description,
            filename
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/seller/dashboard")

    return render_template("seller/add_product.html")

# ---------------- My Products ----------------
@seller.route("/seller/my-products")
def my_products():

    if "seller_id" not in session:
        return redirect("/seller/login")

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
        WHERE SellerId=%s
    """, (session["seller_id"],))

    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "seller/my_products.html",
        products=products
    )
# ---------------- Seller Logout ----------------
@seller.route("/seller/logout")
def logout():

    session.clear()

    return redirect("/seller/login")