import calendar
import datetime

from flask import Blueprint, request, current_app, make_response, jsonify
from app.model.model import User
from app.auth import token_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/login', methods=['POST'])
def login():
    user_dto = request.get_json()
    user = User.query.filter_by(username=user_dto.get('username')).first()
    password_as_bytes = str.encode(user.password)
    try:
        if user and current_app.bcrypt.check_password_hash(password_as_bytes, user_dto.get('password', None)):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(responseObject)), 404
    except Exception as e:
        responseObject = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(responseObject)), 500


@bp.route('/create_new_user', methods=['POST'])
def create_new_user():
    user_dto = request.get_json()
    user = User.query.filter_by(username=user_dto.get('username')).first()
    if not user:
        try:
            pw_hash = current_app.bcrypt.generate_password_hash(user_dto.get("password", None)).decode()
            user = User(username=user_dto.get('username', None), password=pw_hash,
                        name=user_dto.get('name', None), email=user_dto.get('email', None))
            current_app.db.session.add(user)
            current_app.db.session.commit()
            auth_token = user.encode_auth_token(user.id)
            responseObject = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token.decode()
            }

            current_app.db.session.commit()
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return make_response(jsonify(responseObject)), 202


#Get current user entity and all assigned transactions
@bp.route('/current', methods=["GET"])
@token_required
def current(current_user):
    user = current_user
    transaction = current_app.transactions_schema.dump(user.transactions)
    responseObject = {
        'status': 'success',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'name': user.name,
            'email': user.email,
            'balance': user.balance,
            'transactions': transaction
        }
    }
    return make_response(jsonify(responseObject)), 200

#Set balance for current user
@bp.route("/set_balance", methods=['POST'])
@token_required
def set_balance(current_user):
    balance_dto = request.get_json()
    balance = balance_dto.get("balance")
    current_user.balance = float(balance)
    responseObject = {
        'status': 'success',
        'data': {
            'message': 'Balance was successfuly saved'
        }
    }
    current_app.db.session.add(current_user)
    current_app.db.session.commit()
    return make_response(jsonify(responseObject)), 200


#Get daily budget
@bp.route("/daily", methods=["GET"])
@token_required
def get_daily_balance(current_user):
    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    daily_budget = int(current_user.balance / days_in_month)
    responseObject = {
        'status': 'success',
        'data': {
            'daily': daily_budget
        }
    }
    return make_response(jsonify(responseObject)), 200


@bp.route('/ping')
def debug():
    return "Ping"
