from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db, Transaction, Account, User
from sqlalchemy import or_

transaction_bp = Blueprint('transactions', __name__)

@transaction_bp.route('', methods=['GET'])
@jwt_required()
def get_transactions():
    user_id = get_jwt_identity()
    
    # Get query parameters
    account_id = request.args.get('account_id', type=int)
    transaction_type = request.args.get('type')
    
    # Get user's accounts
    user_accounts = Account.query.filter_by(user_id=user_id).all()
    account_ids = [account.id for account in user_accounts]
    
    if not account_ids:
        return jsonify({"transactions": []}), 200
    
    # Base query: transactions where the user's accounts are involved
    query = Transaction.query.filter(
        or_(
            Transaction.from_account_id.in_(account_ids),
            Transaction.to_account_id.in_(account_ids)
        )
    )
    
    # Apply filters
    if account_id:
        if account_id not in account_ids:
            return jsonify({"error": "Unauthorized access to account"}), 403
        query = query.filter(
            or_(
                Transaction.from_account_id == account_id,
                Transaction.to_account_id == account_id
            )
        )
    
    if transaction_type:
        query = query.filter_by(transaction_type=transaction_type)
    
    # Get transactions
    transactions = query.order_by(Transaction.created_at.desc()).all()
    
    return jsonify({
        "transactions": [transaction.to_dict() for transaction in transactions]
    }), 200

@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    user_id = get_jwt_identity()
    
    # Get user's accounts
    user_accounts = Account.query.filter_by(user_id=user_id).all()
    account_ids = [account.id for account in user_accounts]
    
    # Get transaction
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    
    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
    
    # Check if the transaction involves the user's accounts
    if (transaction.from_account_id and transaction.from_account_id not in account_ids) and \
       (transaction.to_account_id and transaction.to_account_id not in account_ids):
        return jsonify({"error": "Unauthorized access to transaction"}), 403
    
    return jsonify(transaction.to_dict()), 200

@transaction_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['transaction_type', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
    
    transaction_type = data['transaction_type']
    amount = float(data['amount'])
    
    if amount <= 0:
        return jsonify({"error": "Amount must be positive"}), 400
    
    # Process based on transaction type
    if transaction_type == 'deposit':
        return handle_deposit(user_id, data)
    elif transaction_type == 'withdrawal':
        return handle_withdrawal(user_id, data)
    elif transaction_type == 'transfer':
        return handle_transfer(user_id, data)
    else:
        return jsonify({"error": "Invalid transaction type"}), 400

def handle_deposit(user_id, data):
    # Validate required fields
    if 'to_account_id' not in data:
        return jsonify({"error": "Destination account is required"}), 400
    
    to_account_id = data['to_account_id']
    amount = float(data['amount'])
    
    # Get account
    account = Account.query.filter_by(id=to_account_id).first()
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    # Check if the account belongs to the user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized access to account"}), 403
    
    # Create transaction
    transaction = Transaction(
        transaction_type='deposit',
        amount=amount,
        to_account_id=to_account_id,
        description=data.get('description', 'Deposit')
    )
    
    # Update account balance
    account.balance += amount
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        "message": "Deposit successful",
        "transaction": transaction.to_dict(),
        "updated_balance": account.balance
    }), 201

def handle_withdrawal(user_id, data):
    # Validate required fields
    if 'from_account_id' not in data:
        return jsonify({"error": "Source account is required"}), 400
    
    from_account_id = data['from_account_id']
    amount = float(data['amount'])
    
    # Get account
    account = Account.query.filter_by(id=from_account_id).first()
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    # Check if the account belongs to the user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized access to account"}), 403
    
    # Check if account has sufficient balance
    if account.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    
    # Create transaction
    transaction = Transaction(
        transaction_type='withdrawal',
        amount=amount,
        from_account_id=from_account_id,
        description=data.get('description', 'Withdrawal')
    )
    
    # Update account balance
    account.balance -= amount
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        "message": "Withdrawal successful",
        "transaction": transaction.to_dict(),
        "updated_balance": account.balance
    }), 201

def handle_transfer(user_id, data):
    # Validate required fields
    if 'from_account_id' not in data:
        return jsonify({"error": "Source account is required"}), 400
    if 'to_account_id' not in data:
        return jsonify({"error": "Destination account is required"}), 400
    
    from_account_id = data['from_account_id']
    to_account_id = data['to_account_id']
    amount = float(data['amount'])
    
    # Get accounts
    from_account = Account.query.filter_by(id=from_account_id).first()
    to_account = Account.query.filter_by(id=to_account_id).first()
    
    if not from_account:
        return jsonify({"error": "Source account not found"}), 404
    if not to_account:
        return jsonify({"error": "Destination account not found"}), 404
    
    # Check if the source account belongs to the user
    if from_account.user_id != user_id:
        return jsonify({"error": "Unauthorized access to source account"}), 403
    
    # Check if account has sufficient balance
    if from_account.balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400
    
    # Create transaction
    transaction = Transaction(
        transaction_type='transfer',
        amount=amount,
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        description=data.get('description', 'Transfer')
    )
    
    # Update account balances
    from_account.balance -= amount
    to_account.balance += amount
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        "message": "Transfer successful",
        "transaction": transaction.to_dict(),
        "source_account_balance": from_account.balance,
        "destination_account_balance": to_account.balance
    }), 201 