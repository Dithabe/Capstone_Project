from django.db import models
from books.models import Book
from users.models import User
from django.utils import timezone

# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transactions')
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)
    deadline= models.DateTimeField(default=timezone.now() + timezone.timedelta(days=14))

    class Meta:
        unique_together = ['user', 'book', 'returned']