from datetime import date
import datetime
from django.http import request
from django.shortcuts import render, redirect
from.models import *
from django.http.response import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def addusers(request):
    if request.method=='POST':
        f=request.POST.get('username')
        f1=request.POST.get('First name')
        f2=request.POST.get('Last name')
        e=request.POST.get('Email')
        m=request.POST.get('Mobile')
        a=request.POST.get('Age')
        psw=request.POST.get('Password')
        User.objects.create_user(username=f,first_name=f1,last_name=f2,email=e,mob=m,age=a,password=psw)
        return render(request,"user/login.html")
    return render(request,"user/signup.html")

def new(request):
    k=User.objects.all()
    return render(request,"user/index.html",{"data":k})

def userlogin(request):
    if request.method=='POST':
        m=request.POST.get('Email')
        ps=request.POST.get('Password')
        user=authenticate(request,email=m,password=ps)
        if user:
            login(request,user)
            return render(request,"user/index.html")
        else:
            return HttpResponse("Invalid User!!")
    return render(request,"user/login.html")

def adminlogin(request):
    if request.method=='POST':
        n=request.POST.get('Email')
        psw=request.POST.get('Password')
        user=authenticate(request,email=n,password=psw)
        if user.is_active and user.is_superuser:
            login(request,user)
            return render(request,"dashboard/index1.html")
        else:
            return HttpResponse("Invalid User!!")
    return render(request,"user/Admin Login.html")

def dashboard1(request):
    return render(request,"dashboard/index1.html")

def dashboard2(request):
    return render(request,"dashboard/index2.html")

def dashboard3(request):
    return render(request,"dashboard/index3.html")

def addcategory(request):
    if request.method=='POST':
        c=request.POST.get('cname')
        n=request.POST.get('nos')
        v=request.POST.get('valid')
        pa=request.POST.get('paid')
        im=request.FILES['image']
        fo=FileSystemStorage()
        im2=fo.save(im.name,im)
        category.objects.create(cname=c,nos=n,valid=v,paid=pa,image=im2)
    return render(request,'dashboard/cate.html')

def addprogram(request):
    k=category.objects.all()
    if request.method=='POST':
        t=request.POST.get('Title')
        e=request.POST.get('Episode')
        v=request.POST.get('Videourl')
        im=request.FILES['image']
        fo=FileSystemStorage()
        im2=fo.save(im.name,im)
        vi=request.FILES['Video']
        fo1=FileSystemStorage()
        vi2=fo1.save(vi.name,vi)
        c=request.POST.get('category')
        c1=category.objects.get(id=c)
        program.objects.create(title=t,Episode=e,videourl=v,image=im2,video=vi2,ca=c1)
        return redirect("get")
    return render (request,'dashboard/prog.html',{"data":k})

def getprogram(request):
    k=program.objects.all()
    if request.method=="POST":
        se=request.POST.get('title')
        res=program.objects.filter(title=se)
        return render(request,"dashboard/tble.html",{'data':res})
    return render(request,"dashboard/tble.html",{"data":k})

def delpro(request,userid):
    x=program.objects.get(id=userid)
    x.delete()
    return redirect("get")

def update_pro(request,userid):
    u=program.objects.filter(id=userid).values()
    a=category.objects.all()
    if request.method=="POST":
        f=request.POST.get('Title')
        p=request.POST.get('Episode')
        i=request.POST.get('video')
        im=request.FILES['image']
        fo=FileSystemStorage()
        im2=fo.save(im.name,im)
        vi=request.FILES['video']
        fo1=FileSystemStorage()
        vi2=fo1.save(vi.name,vi)
        c=request.POST.get('category')
        c1=category.objects.get(id=c)
        u.update(title=f,Episode=p,videourl=i,image=im2,video=vi2,ca=c1)
        return redirect("get")
    return render(request,"dashboard/update.html",{"userdata":u[0],"id":userid,"data":a})


def addcate(request):
    k=maincategory.objects.all()
    if request.method=='POST':
        c=request.POST.get('category')
        c1=category.objects.get(id=c)
        category.objects.create(cat=c1)
    return render(request,"dashboard/cate.html",{"data":k})

def viewuser(request):
    u=User.objects.all()
    if request.method=="POST":
        s3=request.POST.get('name')
        res=User.objects.filter(name=s3)
        return render(request,"dashboard/user.html",{"data":res})
    return render(request,"dashboard/user.html",{"data":u})

def cate(request):
    ca=category.objects.all()
    return render(request,"user/categories.html",{"data":ca})

def act(request,catid):
    k=program.objects.filter(ca__id=catid)
    return render(request,"user/Action.html",{'data':k})

def viewcate(request):
    p=category.objects.all()
    if request.method=="POST":
        s2=request.POST.get('name')
        re=User.objects.filter(name=s2)
        return render(request,"dashboard/cateview.html",{"data":re})
    return render(request,"dashboard/cateview.html",{"data":p})

def sub(request,pid,uid):
    if request.user.is_authenticated:
        p=maincategory.objects.filter(id=pid)
        u=User.objects.filter(id=uid).values()
        print("###########################")
        print(p)
        return render(request,"user/sub.html",{'data':u,'data2':p[0]})
    else:
        return redirect('pur')


def purch(request):
    if request.method=='POST':
        u=request.POST.get('email')
        ca=request.POST.get('cname')
        mo=request.POST.get('mob')
        dat=datetime.datetime.today()        
        cobj=maincategory.objects.get(id=ca)
        uobj=User.objects.get(email=u)
        p=cobj.price
        end_date=dat + datetime.timedelta(days=30)
        order.objects.create(ct=cobj,us=uobj,price=p,date=dat,validity=end_date)
        return render(request,"user/success.html")
    return render(request,"user/plan 2.html")

def orders(request):
    u=order.objects.all()
    if request.method=="POST":
        s3=request.POST.get('name')
        res=User.objects.filter(name=s3)
        return render(request,"dashboard/order.html",{"data":res})
    return render(request,"dashboard/order.html",{"data":u})