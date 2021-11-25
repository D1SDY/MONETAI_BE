from flask import request, jsonify, make_response
from functools import wraps
from app.model.model import User
from datetime import datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            payload = User.decode_auth_token(token)
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        now = datetime.now()
        exp = datetime.fromtimestamp(payload.get("exp", None))
        if now > exp:
            return jsonify({'message': 'Token has expired'}), 401
        current_user = User.query.filter_by(id=payload).first()
        return f(current_user, *args, **kwargs)
    return decorated