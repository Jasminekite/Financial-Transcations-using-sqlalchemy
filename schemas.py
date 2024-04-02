from config import ma

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'account_name', 'username', 'first_name', 'last_name', 'email', 'mobile_no', 'pan_card', 'balance', 'add_on', 'update_on')

class TransactionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'amount', 'transaction_type', 'timestamp')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
transaction_schema = TransactionSchema()
transactions_schema = TransactionSchema(many=True)