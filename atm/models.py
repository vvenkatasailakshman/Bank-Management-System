from django.db import models

from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
# Create your models here.

class Account(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.PositiveBigIntegerField()
    email_id = models.EmailField(null=True, blank=True)
    account_number = models.BigIntegerField(unique = True, editable=False)
    encrypted_pin = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    otp = models.CharField(max_length=4, blank=True, null=True) 
    otp_created_at = models.DateTimeField(blank=True, null=True)

    def set_pin(self,raw_pin):
        self.encrypted_pin = make_password(raw_pin)
        self.save()

    def check_pin(self,raw_pin):
        return check_password(raw_pin,self.encrypted_pin)
    
    def generate_otp(self):
        import random
        self.otp = f"{random.randint(1000, 9999)}"
        self.otp_created_at = datetime.now()
        self.save()

    def verify_otp(self, otp_input):
        if self.otp == otp_input and self.otp_created_at > datetime.now() - timedelta(minutes=10):
            return True
        return False
    
    def clear_otp(self):
        self.otp = None
        self.otp_created_at = None
        self.save()

    def __str__(self):
        return f'Account {self.account_number}'
    

    

    def save(self, *args, **kwargs):
        if not self.pk:
            last_account = Account.objects.order_by('-account_number').first()
            if last_account:
                self.account_number = last_account.account_number + 1
            else:
                self.account_number = 12345678911
        super().save(*args, **kwargs)                