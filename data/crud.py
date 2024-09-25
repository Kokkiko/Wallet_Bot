import datetime, uuid
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
a = app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:b269bba3@localhost/fe"
db = SQLAlchemy(app)


class users(db.Model):
    telegram_id = db.Column(db.BigInteger, primary_key=True)
    user_quid = db.Column(db.String(120), default=str(uuid.uuid4()))


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = users(telegram_id=data["telegram_id"], user_quid=data["user_quid"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify("New user created")


@app.route("/users/<telegram_id>", methods=["GET"])
def get_user(telegram_id):
    user = users.query.get(telegram_id)
    return jsonify(user.telegram_id)


class addresses(db.Model):
    telegram_id = db.Column(db.BigInteger, primary_key=True)
    address = db.Column(db.String(120))
    private_key = db.Column(db.String(120))


@app.route("/addresses", methods=["POST"])
def create_address():
    data = request.get_json()
    new_address = addresses(
        telegram_id=data["telegram_id"],
        address=data["address"],
        private_key=data["private_key"],
    )
    db.session.add(new_address)
    db.session.commit()
    return jsonify("New address created")


@app.route("/addresses/<telegram_id>", methods=["GET"])
def get_address(telegram_id):
    Address = addresses.query.get(telegram_id)
    return jsonify(Address.address, Address.private_key)


class transactions(db.Model):
    id = db.Column(db.Integer)
    transaction_quid = db.Column(db.String(200), primary_key=True, default=uuid.uuid1())
    telegram_id = db.Column(db.BigInteger)
    to = db.Column(db.String(120))
    From = db.Column(db.String(120))
    type = db.Column(db.String(50))
    amount = db.Column(db.String(200))
    transaction_hash = db.Column(db.String(200))
    gasPrice = db.Column(db.String(200))
    timestamp = db.Column(db.String(500))


@app.route("/transactions", methods=["POST"])
def new_transaction():
    data = request.get_json()
    current_time = datetime.datetime.now()
    new_transaction = transactions(
        telegram_id=data["telegram_id"],
        to=data["to"],
        From=data["from"],
        type=data["type"],
        amount=data["amount"],
        transaction_hash=data["transaction_hash"],
        gasPrice=data["gasPrice"],
        timestamp=current_time,
    )
    db.session.add(new_transaction)
    db.session.commit()
    return jsonify("New transaction done!")
