from flask import Flask, redirect
from routes.customer import customer

app = Flask(__name__)

app.register_blueprint(customer)

@app.route("/")
def home():
    return redirect("/register")

if __name__ == "__main__":
    app.run(debug=True)

app.secret_key = "easymart123"