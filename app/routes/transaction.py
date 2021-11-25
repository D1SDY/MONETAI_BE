from flask import Blueprint, request, current_app, make_response, jsonify
from app.model.model import Transaction, Category
from app.schema.shemas import transactions_schema
from app.auth import token_required

bp = Blueprint('transaction', __name__, url_prefix='/transaction')


#Add new transaction to user account, also add it to relevant category
@bp.route('/new', methods=['POST'])
@token_required
def create_new_transaction(current_user):
    transaction_dto = request.get_json()
    category = Category.query.filter_by(id=transaction_dto.get('category')).first()
    transaction = Transaction(title=transaction_dto.get('title', None),
                              description=transaction_dto.get('description', None),
                              location=transaction_dto.get('location', None),
                              total=transaction_dto.get('total', None), state=transaction_dto.get('state', None),
                              date=transaction_dto.get('date', None), duration=transaction_dto.get('duration', None)
                              )
    transaction.category_id = category.id
    transaction.user_id = current_user.id
    current_user.transactions.append(transaction)
    category.transactions.append(transaction)
    responseObject = {
        'status': 'success',
        'data': {
            'message': 'Transaction was successfuly saved'
        }
    }
    current_app.db.session.add(transaction)
    current_app.db.session.add(current_user)
    current_app.db.session.add(category)
    current_app.db.session.commit()
    return make_response(jsonify(responseObject)), 200


#Get all transactions assigned to user
@bp.route('/all', methods=['GET'])
@token_required
def get_all_for_user(current_user):
    transactions = transactions_schema.dump(current_user.transactions)
    responseObject = {
        'status': 'success',
        'data': {
            "transactions": transactions
        }
    }
    return make_response(jsonify(responseObject)), 200


#Get all transactions filtered by date
@bp.route('/date', methods=['POST'])
@token_required
def get_all_transactions_by_date(current_user):
    transaction_dto = request.get_json()
    looking_date = transaction_dto.get('date')
    looking_date = looking_date[:10]
    transactions = current_user.transactions
    transactions = transactions_schema.dump(transactions)
    result = []
    for transaction in transactions:
        for key in transaction:
            if key == "date":
                date = transaction.get(key)
                if date is not None:
                    date = date[:10]
                    if date == looking_date:
                        result.append(transaction)
    responseObject = {
        'status': 'success',
        'data': {
            "transactions": result
        }
    }
    return make_response(jsonify(responseObject)), 200


@bp.route('/ping')
def debug():
    return "Ping"
