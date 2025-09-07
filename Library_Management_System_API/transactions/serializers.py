from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'book', 'checkout_date', 'deadline', 'return_date', 'returned']
        read_only_fields = ['id', 'checkout_date']

class CreateTransactionSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)
    deadline = serializers.DateTimeField(required=True)

class CheckoutSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    user_id = serializers.IntegerField()