from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import auth


class User(auth.models.User):
    PLAN_CHOICES = (
    ('startup', 'Startup'),
    ('pro','Pro'),
    ('enterprise','Enterprise'),
    )
    plan = models.CharField(max_length = 12,choices=PLAN_CHOICES,default='startup')
    credits_bought=models.IntegerField(default=0)
    plan_order_id=models.CharField(max_length=50)    
    credit_order_id=models.CharField(max_length=50)    
    last_plan_bought=models.DateTimeField(auto_now_add=True)
    last_credits_bought=models.DateTimeField(auto_now_add=True)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id=models.CharField(max_length=50)
    amount=models.IntegerField()
    quantity=models.IntegerField()
    bought_on=models.DateTimeField(auto_now_add=True)
    is_paid=models.BooleanField(default=False)





