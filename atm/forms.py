from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['first_name','middle_name','last_name','email_id','phone_number','pin','balance']

class PinForm(forms.Form):
    account_number = forms.IntegerField(max_value=11)
    pin = forms.CharField(widget=forms.PasswordInput)

class transfer(forms.Form):
    accn_num = forms.IntegerField(max_value=11)
    amount = forms.IntegerField()