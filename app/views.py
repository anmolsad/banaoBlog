from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Account

# Create your views here.
def register(request):
    if request.user.is_authenticated:
            return redirect("bloghome")
    if request.method =="POST":
        username= request.POST.get('username')
        email= request.POST.get('email')
        password= request.POST.get('password')
        confirm_pass= request.POST.get('confirm_pass')
        fname= request.POST.get('fname')
        lname= request.POST.get('lname')
        image=request.FILES.get('profile')
        address= request.POST.get('line')
        city= request.POST.get('city')
        state= request.POST.get('state')
        pincode= request.POST.get('pincode')
        checkbox=request.POST.get('checkbox')
            

        if len(password)<3:
            messages.error(request,"password must be at least 3 character")
            return redirect('register')
        if password!=confirm_pass:
            messages.error(request,"Password does not match")
            return redirect('register')
        
        get_all_users=User.objects.filter(username=username)
        if get_all_users:
            messages.error(request,"username already exist")
            return redirect('register')
    
        
            

        new_user=User.objects.create_user(username=username,email=email,password=password)
        new_user.first_name=fname
        new_user.last_name=lname
        new_user.save()
        if checkbox=="doctor":
       
            new_account=Account.objects.create(user=new_user,image=image,address=address,city=city,state=state,pincode=pincode,doctor=checkbox)
            new_account.save()
            messages.success(request,'doctor successfully created')
            return redirect('login')
        else:
            new_account=Account.objects.create(user=new_user,image=image,address=address,city=city,state=state,pincode=pincode)
            new_account.save()
            messages.success(request,'user successfully created')
            return redirect('login')
    return render(request,'app/register.html',{})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect("bloghome")
    if request.method=='POST':
        username=request.POST.get('uname')
        password= request.POST.get('pass')

        validate_user=authenticate(username=username,password=password)
        if validate_user is not None:
            login(request,validate_user)
            return redirect('bloghome')
        else:
            messages.error(request,'user does not exist')
            return redirect('login')
    
    return render(request,'app/login.html')
@login_required(login_url='login')
def home(request):
    users=Account.objects.filter(user__username=request.user.username)

    return render(request,'app/home.html',{"users":users})

@login_required(login_url='login')
def logoutview(request):
    logout(request)
    return redirect('login')
