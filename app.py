from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transactions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------- MODELS ----------
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    currency = db.Column(db.String(10), default='USD')
    date = db.Column(db.Date, default=datetime.utcnow)
    description = db.Column(db.String(200))

with app.app_context():
    db.create_all()

# ---------- ROUTES ----------
@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running!"})

@app.route("/add", methods=["POST"])
def add_transaction():
    data = request.json
    t = Transaction(
        username=data.get("username"),
        amount=data.get("amount"),
        category=data.get("category"),
        currency=data.get("currency", "USD"),
        description=data.get("description")
    )
    db.session.add(t)
    db.session.commit()
    return jsonify({"message": "Transaction added successfully!"})

@app.route("/transactions/<username>", methods=["GET"])
def get_transactions(username):
    transactions = Transaction.query.filter_by(username=username).all()
    result = [
        {
            "id": t.id,
            "amount": t.amount,
            "category": t.category,
            "currency": t.currency,
            "date": t.date.strftime("%Y-%m-%d"),
            "description": t.description,
        }
        for t in transactions
    ]
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
