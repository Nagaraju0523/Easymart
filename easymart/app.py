from flask import Flask, redirect
from routes.customer import customer
from routes.seller import seller
from routes.admin import admin
from flask import Flask, render_template

app = Flask(__name__)

# Secret key for session
app.secret_key = "easymart123"

# Register customer blueprint
app.register_blueprint(customer)
app.register_blueprint(seller)

# Home page
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)