from flask import Flask, jsonify, request
from config import app, jwt
from models import User, Transaction
from schemas import user_schema, users_schema
from schemas import transaction_schema, transactions_schema
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from config import db

# Define a dictionary to store user credentials (in memory)
users = {
    'user1': 'password1',
    'user2': 'password2'
}



@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username is None or password is None:
        return jsonify({'error': 'Missing username or password'}), 400

    if username not in users or users[username] != password:
        return jsonify({'error': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    expiry_seconds = app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
    return jsonify(access_token=access_token, expires_in=expiry_seconds), 200

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/userss', methods=['POST'])
def add_user():
    try:
        account_name = request.json['account_name']
        username = request.json['username']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        email = request.json['email']
        mobile_no = request.json['mobile_no']
        pan_card = request.json['pan_card']
    except KeyError:
        return jsonify({'error': 'Missing required fields (account_name, username, first_name, last_name, email, mobile_no, pan_card)'}), 400

    new_user = User(account_name, username, first_name, last_name, email, mobile_no, pan_card)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

@app.route('/userss', methods=['GET'])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result)

@app.route('/transactions', methods=['POST'])
def add_transaction():
    try:
        user_id = request.json['user_id']
        amount = request.json['amount']
        transaction_type = request.json['transaction_type']
    except KeyError:
        return jsonify({'error': 'Missing required fields (user_id, amount, transaction_type)'}), 400

    new_transaction = Transaction(user_id, amount, transaction_type)
    db.session.add(new_transaction)
    db.session.commit()

    return transaction_schema.jsonify(new_transaction), 201

@app.route('/transactions', methods=['GET'])
def get_transactions():
    all_transactions = Transaction.query.all()
    result = transactions_schema.dump(all_transactions)
    return jsonify(result)


# Endpoint for deposits
@app.route('/deposits', methods=['POST'])
def make_deposit():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')

    if not user_id or not amount:
        return jsonify({'error': 'User ID and amount are required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    user.balance += amount
    db.session.commit()

    transaction = Transaction(user_id=user_id, amount=amount, transaction_type='deposit')
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Deposit successful'}), 201

# Endpoint for withdrawals
@app.route('/withdrawals', methods=['POST'])
def make_withdrawal():
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')

    if not user_id or not amount:
        return jsonify({'error': 'User ID and amount are required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    if user.balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400

    user.balance -= amount
    db.session.commit()

    transaction = Transaction(user_id=user_id, amount=amount, transaction_type='withdrawal')
    db.session.add(transaction)
    db.session.commit()

    return jsonify({'message': 'Withdrawal successful'}), 201

# Endpoint for transfers
@app.route('/transfers', methods=['POST'])
def make_transfer():
    data = request.json
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    amount = data.get('amount')

    if not sender_id or not recipient_id or not amount:
        return jsonify({'error': 'Sender ID, recipient ID, and amount are required'}), 400

    sender = User.query.get(sender_id)
    recipient = User.query.get(recipient_id)

    if not sender or not recipient:
        return jsonify({'error': 'Sender or recipient not found'}), 404

    try:
        amount = float(amount)
    except ValueError:
        return jsonify({'error': 'Invalid amount'}), 400

    if sender.balance < amount:
        return jsonify({'error': 'Insufficient balance'}), 400

    sender.balance -= amount
    recipient.balance += amount
    db.session.commit()

    sender_transaction = Transaction(user_id=sender_id, amount=amount, transaction_type='transfer_sent')
    recipient_transaction = Transaction(user_id=recipient_id, amount=amount, transaction_type='transfer_received')
    db.session.add(sender_transaction)
    db.session.add(recipient_transaction)
    db.session.commit()

    return jsonify({'message': 'Transfer successful'}), 201

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=6000)
