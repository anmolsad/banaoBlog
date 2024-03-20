from django.shortcuts import render,redirect


from app.models import Account
from .models import Post,Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
@login_required(login_url="login") 
def bloghome(request):
    users = request.user #the user
    account=Account.objects.get(user=users)
    posts=Post.objects.all().filter(draft=False).order_by("-created_on")
    categories=Category.objects.all()
    context={
        "posts":posts,
        "user":account,
        "categories":categories,
    }
    return render(request,"blog/blog.html",context)
@login_required(login_url="login")
def createblog(request):
    users = request.user #the user
    account=Account.objects.get(user=users)
    if account.doctor == None:
        return redirect('bloghome')

    

    
    if request.method=='POST':
        title=request.POST.get('title')
        image= request.FILES.get('image')
        summary= request.POST.get('summary')
        category= request.POST.get('category')
        content= request.POST.get('content')
        author=account.user.email
        draft= request.POST.get('draft')
        

        categories=Category.objects.get(name=category)
        if draft=="True":

            blogpost=Post.objects.create(title=title,image=image,summary=summary,categories=categories,content=content,author=author,draft=True)
            blogpost.save()
        else:
            blogpost=Post.objects.create(title=title,image=image,summary=summary,categories=categories,content=content,author=author,draft=False)
            blogpost.save()

    categories=Category.objects.all()
    context={
        "categories":categories,
        "user":account,
    }
    return render(request,"blog/createblog.html",context)

@login_required(login_url="login")
def postcategory(request,category):
    users = request.user #the user
    account=Account.objects.get(user=users)
    categories=Category.objects.all()
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category": category,
        "posts": posts,
        "categories":categories,
        "user":account,

    }
    return render(request,"blog/blog.html",context)

@login_required(login_url="login")
def blogdetails(request,id):
    posts = Post.objects.get(id=id)
    context={
        'post':posts,
    }
    return render(request,"blog/blogdetail.html",context)

@login_required(login_url="login")
def blogdraft(request):
    
    users = request.user #the user
    account=Account.objects.get(user=users)
    posts = Post.objects.filter(author=account.user.email,draft=True)
    context={
        'posts':posts,
    }
    return render(request,"blog/blogdraft.html",context)

@login_required(login_url="login")
def removedraft(request,id):
    if id:
        post = Post.objects.get(id=id)
        post.draft=False
        post.save()
        return redirect('blogdraft')

