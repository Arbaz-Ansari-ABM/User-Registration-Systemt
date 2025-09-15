from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    course = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)

@app.route("/view-users")
def view_users():
    users = User.query.all()
    return render_template("view_users.html", users=users)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided."}), 400

    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    contact = data.get("contact", "").strip()
    email = data.get("email", "").strip().lower()
    course = data.get("course", "").strip()
    address = data.get("address", "").strip()

    if not all([first_name, last_name, contact, email, course, address]):
        return jsonify({"message": "Please fill in all required fields."}), 400

    try:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "This email is already registered."}), 400

        user = User(
            first_name=first_name,
            last_name=last_name,
            contact=contact,
            email=email,
            course=course,
            address=address
        )

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": f"Hello {user.first_name}, your registration is successful!"})

    except Exception as e:
        print("Server error:", e)
        return jsonify({"message": "Something went wrong. Please try again."}), 500

if __name__ == "__main__":
    app.run(debug=True)
