from app.ma import ma
from app.model.model import Transaction, Category


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True
        load_only = ("store",)
        include_fk = True


transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)


class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        load_only = ("store",)
        include_fk = True


category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
