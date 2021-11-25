from flask import Blueprint, request, current_app, make_response, jsonify
from app.schema.shemas import categories_schema
from app.model.model import Category
from app.auth import token_required
bp = Blueprint('categories', __name__, url_prefix='/categories')


#Create new catergory with name, icon, color sended from frontend
@bp.route('/new', methods=['POST'])
@token_required
def create_new_category(current_user):
    category_dto = request.get_json()
    category = Category(name=category_dto.get('name'), icon=category_dto.get('icon', None),
                        color=category_dto.get('color', None))
    current_user.categories.append(category)
    category.user_id = current_user.id
    current_app.db.session.add(current_user)
    current_app.db.session.add(category)
    current_app.db.session.commit()
    responseObject = {
        'status': 'success',
        'data': {
            'message': 'Category was successfuly saved'
        }
    }
    return make_response(jsonify(responseObject)), 200


#Get all categories assigned to current user
@bp.route('/all', methods=['GET'])
@token_required
def get_all_categories_for_user(current_user):
    categories = categories_schema.dump(current_user.categories)
    responseObject = {
        'status': 'success',
        'data': {
            "categories": categories
        }
    }
    return make_response(jsonify(responseObject)), 200



@bp.route('/ping')
def debug():
    return "Ping"
