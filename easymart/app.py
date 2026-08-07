from flask import Flask, render_template
from routes.customer import customer
from routes.seller import seller
from routes.admin import admin

app = Flask(__name__)

# Secret key for session
app.secret_key = "easymart123"

# Register Blueprints
app.register_blueprint(customer)
app.register_blueprint(seller)
app.register_blueprint(admin)

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)