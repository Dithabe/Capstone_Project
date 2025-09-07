from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Transaction
from .serializers import TransactionSerializer, CheckoutSerializer
from books.models import Book
from users.models import User

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = get_object_or_404(Book, pk=serializer.validated_data['book_id'])
        user = get_object_or_404(User, pk=serializer.validated_data['user_id'])
        
        if user != request.user and not request.user.is_staff:
            raise PermissionDenied("You may only checkout your own books")
        
        # If not books are available, printout an error message
        if book.copies_available <= 0:
            return Response(
                {'error': 'No books available'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if Transaction.objects.filter(user=user, book=book, is_returned=False).exists():
            return Response(
                {'error': 'This books is has already been checked out. Try again after a few days'},
                status=status.HTTP_400_BAD_REQUEST
            )

        transaction = Transaction.objects.create(
            user=user,
            book=book,
            due_date=datetime.now() + timedelta(days=14),
            is_returned=False
        )

        # Update copies count
        book.copies_available -= 1
        book.save()

        return Response(
            TransactionSerializer(transaction).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        transaction = get_object_or_404(Transaction, pk=pk)

        # Validating the user
        if transaction.user != request.user and not request.user.is_staff:
            raise PermissionDenied("You may only return your own books")

        if transaction.is_returned:
            return Response(
                {'error': 'This book is available in the library'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # This part outlines the return process
        transaction.is_returned = True
        transaction.return_date = datetime.now()
        transaction.save()

        # Update copies count
        transaction.book.copies_available += 1
        transaction.book.save()

        return Response(
            TransactionSerializer(transaction).data,
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        raise PermissionDenied()
    