from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db, Account, User
import uuid

account_bp = Blueprint('accounts', __name__)

@account_bp.route('', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = get_jwt_identity()
    
    # Get accounts for the user
    accounts = Account.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        "accounts": [account.to_dict() for account in accounts]
    }), 200

@account_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    user_id = get_jwt_identity()
    
    # Get account
    account = Account.query.filter_by(id=account_id).first()
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    # Check if the account belongs to the user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized access to account"}), 403
    
    return jsonify(account.to_dict()), 200

@account_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    if 'account_type' not in data:
        return jsonify({"error": "Account type is required"}), 400
    
    # Generate unique account number
    account_number = f"ACC-{uuid.uuid4().hex[:8].upper()}"
    
    # Create new account
    new_account = Account(
        account_number=account_number,
        account_type=data['account_type'],
        balance=data.get('initial_balance', 0.0),
        user_id=user_id
    )
    
    db.session.add(new_account)
    db.session.commit()
    
    return jsonify({
        "message": "Account created successfully",
        "account": new_account.to_dict()
    }), 201

@account_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Get account
    account = Account.query.filter_by(id=account_id).first()
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    # Check if the account belongs to the user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized access to account"}), 403
    
    # Update account fields
    if 'account_type' in data:
        account.account_type = data['account_type']
    if 'is_active' in data:
        account.is_active = data['is_active']
    
    db.session.commit()
    
    return jsonify({
        "message": "Account updated successfully",
        "account": account.to_dict()
    }), 200

@account_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    user_id = get_jwt_identity()
    
    # Get account
    account = Account.query.filter_by(id=account_id).first()
    
    if not account:
        return jsonify({"error": "Account not found"}), 404
    
    # Check if the account belongs to the user
    if account.user_id != user_id:
        return jsonify({"error": "Unauthorized access to account"}), 403
    
    # Check if account has balance
    if account.balance > 0:
        return jsonify({"error": "Cannot delete account with positive balance"}), 400
    
    # Delete account
    db.session.delete(account)
    db.session.commit()
    
    return jsonify({
        "message": "Account deleted successfully"
    }), 200 