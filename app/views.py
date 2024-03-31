from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Account

# Create your views here.

import datetime
from datetime import timedelta
import pytz

# import pickle
import os.path
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

start_time =0
end_time=0
  
scopes = ['https://www.googleapis.com/auth/calendar']

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
credential_file=str(CURR_DIR)+'/credentials.json'
def bookform(request,pk):
    form = Account.objects.get(id=pk)
    if request.method == 'POST':
        form = Account.objects.get(id=pk)
        req = request.POST['req']
        start = request.POST['start']
        time = request.POST['time']
        email = request.POST['email']
        starts = start +' '+ time +':' '00'
    
        start_time = datetime.datetime.strptime(starts,"%Y-%m-%d %H:%M:%S")
        end_time  = start_time + timedelta(minutes=45)
        context = { 'req':req,'start':start,'time':time,'start_time':start_time, 'end_time':end_time,'email':email,'form':form}
        return  render(request, 'app/confirm.html',context)
        

    
    return render(request,'app/bookform.html',{'form':form})

def confirm(request):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_file, scopes
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds) 
        if request.method == 'POST':
            req = request.POST['required']
            start = request.POST['starts']
            time = request.POST['time']
            email = request.POST['email']
            start = start +' '+ time +':' '00' 
            start_time = datetime.datetime.strptime(start,"%Y-%m-%d %H:%M:%S")
            end_time  = start_time + timedelta(minutes=45)
            timezone = 'Asia/Kolkata'
            print("Gsfgfd",start_time.isoformat(),'vdfdf',end_time.isoformat())
            print("dsdv",req)
            print("Gfdg",email),
            event = (
            service.events()
            .insert(
                calendarId="primary",
                body={
                    "summary": req,
                
                    "start": {"dateTime": start_time.isoformat(),
                    'timeZone': timezone,
                
                    
                    },
                    "end": {
                        "dateTime": end_time.isoformat(),
                        'timeZone': timezone,
                    },
                    "attendees":[{"email":email}
                    
                    ]
                },
            )
            .execute()
            )
            
            return redirect('bloghome')
    except HttpError as error:
        print(f"An error occurred: {error}")
    
    return render(request,'app/confirm.html')

# def viewevent(request):
#     service = build("calendar", "v3", credentials=credentials)
#     now = datetime.datetime.utcnow().isoformat() + 'Z' 
#     events_result = service.events().list(calendarId='primary', timeMin=now,
#                                               maxResults=10, singleEvents=True,
#                                               orderBy='startTime').execute()
#     events = events_result.get('items', [])

#     if not events:
#         print('No upcoming events found.')
#         return

#         # Prints the start and name of the next 10 events
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         email = event['attendees'][0:]
#         print(start,email)

#     return render(request,'viewevent.html',{'form':start})

def doctor(request):
    doctors = Account.objects.filter(doctor='doctor')
    print(doctors)

    return render(request,'app/doctor.html',{'doctors':doctors})



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
