from django.shortcuts import render, redirect, HttpResponse

from django.contrib import messages
from .models import Account
from .forms import AccountForm, PinForm
import email
from django.core.mail import send_mail
from random import randint

# Create your views here.

def create_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.set_pin(form.cleaned_data['pin'])
            account.save()
            print(account)
            return redirect('bridge')
        
    else:
        form = AccountForm()
    return render(request, 'create.html', {'form':form})


def bridge(request):
    # Assuming you want to get the first account number from the database
    account = Account.objects.first()  # Gets the first Account instance
    
    context = {
        'account': account
    }
    
    return render(request, 'bridge.html', context)



def validate_pin(request):
    balance = None
    id = None
    if request.method == "POST":
        form = PinForm(request.POST)
        
        print("one")
        account_number = request.POST['account_number']
        pin = request.POST['pin']
        try:
            account = Account.objects.get(account_number = account_number)
            if account.check_pin(pin):
                balance = account.balance
                id  = account.id
            else:
                messages.error(request,'Invalid PIN')
        except Account.DoesNotExist:
            messages.error(request,'Account not found')

    else:
        form = PinForm()

    return render(request,'validate.html',{'form':form, 'balance': balance,'id':id})

def transfer(request,pk):
    data = Account.objects.get(id = pk)
    balance  =   data.balance
    if request.method == 'POST':
        acc_ = request.POST.get('accountNumber')
        try:
            data1 = Account.objects.get(account_number = acc_)
            print(data,data1)

            if data1:
                amount = request.POST.get('amount')
                # if data.account_number == int(acc_):
                #     print("acc")
                    # messages.error(request,'Unable to transfer to the same check your account')
                if int(data.account_number) != int(acc_):
                    if int(amount) < balance:
                        data1.balance += int(amount)
                        data1.save()
                        print(data1.balance)
                        data.balance -= int(amount)
                        data.save()
                        print(data.balance)
                        # messages.success(request,'Transaction Succesfully')
                        return redirect('transfersuccess')
                    else:
                        messages.error(request,'Insufficient Balance')
                    print("one")
                    
                else:
                    messages.error(request,'Unable to transfer to the same check your account') 
        except Account.DoesNotExist as e:
            print(e)
            messages.error(request,"Account doesn't exists")

    return render(request,'transfer.html')    

def deposit(request,pk):
    # pk = 1
    account = Account.objects.get(id = pk)
    if request.method == "POST":
        amt  = int(request.POST.get('amount'))
        account.balance = account.balance + amt
        account.save()
        messages.success(request,'Deposited succesfully')

    context = {
        'data':account
    }

    return render(request,'deposit.html',context)   

def withdrawal(request,pk):
    # pk = 1
    account = Account.objects.get(id = pk)
    if request.method == "POST":
        amt = int(request.POST.get('amount'))
        if account.balance >= amt:
            account.balance = account.balance - amt
            account.save()
            messages.success(request,'withdrawal succesfully')
        
        else:
            messages.error(request, 'Insufficient funds to withdraw.')
            

    context = {
        'data' : account
    }  

    return render(request,'withdrawal.html',context)    


def transfersuccess(request):
    return render(request,'transfersuccess.html')



def forgot_pin(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            account = Account.objects.get(email_id = email)
            otp = randint(1000, 9999)
            account.otp = otp
            account.save()
           

            # Send OTP to email
            send_mail(
                'This OTP for your Account PIN Reset',
                f'Your OTP is: {otp}\nFrom the Prosperity Bank',
                'rsuvamdora22101@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['email'] = email
            return redirect(f'verify_otp/{account.id}')
        except Account.DoesNotExist:
            messages.error(request, 'Account with this email does not exist.')
 
    return render(request, 'forgot_pin.html')


def verify_otp(request,pk):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        # print(otp_entered)
        # email = request.session.get('email')
        try:

            account = Account.objects.get(id = pk)
            # account = Account.objects.get(email_id = email, otp = otp_entered)
            # print(account)
            if account.otp == otp_entered:
                return redirect('reset_pin')
            else:
                print(account.otp, otp_entered)
        except Account.DoesNotExist:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'verify_otp.html')


def reset_pin(request):
    if request.method == 'POST':
        
            id = 2
            account = Account.objects.get(id = id)
            new_pin = request.POST.get('new_pin')
            confirm_pin = request.POST.get('confirm_pin')
            if account.check_pin('pin') != new_pin:
                if new_pin == confirm_pin:
                    # account = Account.objects.get(id=id)
                    account.set_pin(new_pin)
                    account.otp = None  # Clear the OTP after use
                    account.save()
                    messages.success(request, 'PIN successfully reset.')
                    return redirect('validate_pin')
                else:
                    messages.error(request, 'PINs do not match.')
            else:
                messages.error(request,"Please don't give old pin again")
        
    return render(request, 'reset_pin.html')


