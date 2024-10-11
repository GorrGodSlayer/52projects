from django.db import models
from core.models import User
from tables.models import Table
from menu.models import MenuItem, Addition

class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
        ('paid', 'Paid'),
    ])

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()

class OrderItemAddition(models.Model):
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='additions')
    addition = models.ForeignKey(Addition, on_delete=models.CASCADE)
    quantity = models.IntegerField()
