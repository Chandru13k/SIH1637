from django.db import models
from users.models import User
from database.models import Listings
import uuid
status=(("Pending","Pending"),("Completed","Completed"),("Cancelled","Cancelled"))

# Create your models here.
class Transaction(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name="transactions")
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    listing=models.ForeignKey(Listings,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=status,default="Pending")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=("buyer","listing")
    def __str__(self):
        return f"{self.buyer} - {self.listing} - {self.status}"

class Order(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)    
    transaction=models.ForeignKey(Transaction,on_delete=models.CASCADE)
    status=models.CharField(max_length=20,choices=status,default="Pending")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.transaction} - {self.status}"

class Payment(models.Model):
    id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    status=models.CharField(max_length=20,choices=status,default="Pending")
    transaction_id=models.CharField(max_length=255,unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.order} - {self.amount} - {self.status}"
    