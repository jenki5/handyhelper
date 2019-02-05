from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from apps.handyhelper.models import *
from . import views
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'handyhelper/index.html')

def process_register(request):
    print('8'*80)
    print("I'm in the register function")
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user_hashpw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = user_hashpw)
        user = User.objects.last()
        request.session['logged_in'] = True
        request.session['first_name'] = user.first_name
        request.session['user_id'] = user.id
        print(User.objects.all().values())
    return redirect('/dashboard')

def process_login(request):
    user = User.objects.get(email = request.POST['email'])
    print('*'*80)
    print(user.__dict__)
    request.session['user_id'] = user.id
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['logged_in'] = True
        request.session['first_name'] = user.first_name
        request.session['user_id'] = user.id
        if request.session['login_fail']:
            request.session['login_fail'] = ""
        return redirect('/dashboard')
    else:
        request.session['login_fail'] = "Failed to log you in. Please check email and password"
        print(request.session['login_fail'])
    return redirect('/')

def dashboard(request):
    if request.session['logged_in']:
        request.session['login_fail'] = ""
        context ={
            'jobs': OpenJob.objects.all(),
            'myjobs': UserJob.objects.filter(job_doer = User.objects.get(id = request.session['user_id']))
        }
        return render(request, 'handyhelper/dashboard.html', context)
    else:
        request.session['login_fail'] = "You are not logged in. Please sign in here or create an account."
        return redirect('/')


def logout(request):
    request.session['logged_in'] = False
    request.session['login_fail'] = ""
    return redirect('/')

def add_job(request):
    if request.session['logged_in']:
        request.session['login_fail'] = ""
        return render(request, 'handyhelper/add_job.html')
    else:
        request.session['login_fail'] = "You are not logged in. Please sign in here or create an account."
    return redirect('/')

def process_add_job(request):
    errors = User.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_job')
    else:
        OpenJob.objects.create(title = request.POST['title'], desc = request.POST['desc'], location = request.POST['location'], job_adder = User.objects.get(id = request.session['user_id']))
        print(OpenJob.objects.all().values())
    return redirect('/dashboard')

def view_job(request, id):
    if request.session['logged_in']:
        request.session['login_fail'] = ""
        return render(request, 'handyhelper/view_job.html', {'job': OpenJob.objects.get(id = id)})
    else:
        request.session['login_fail'] = "You are not logged in. Please sign in here or create an account."
    return redirect('/')

def add(request, id):
    job = OpenJob.objects.get(id = id)
    UserJob.objects.create(title = job.title, desc = job.desc, location = job.location, job_doer = User.objects.get(id = request.session['user_id']))
    job.delete()
    return redirect('/dashboard')

def edit_job(request, id):
    if request.session['logged_in']:
        request.session['login_fail'] = ""
        return render(request, 'handyhelper/edit_job.html', {'job': OpenJob.objects.get(id = id)})
    else:
        request.session['login_fail'] = "You are not logged in. Please sign in here or create an account."
    return redirect('/')

def cancel(request, id):
    job = OpenJob.objects.get(id = id)
    job.delete()
    return redirect('/dashboard')

def process_edit_job(request, id):
    errors = User.objects.job_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/edit/'+id)
    else:
        job = OpenJob.objects.get(id = id)
        job.title = request.POST['title']
        job.desc = request.POST['desc']
        job.location = request.POST['location']
        job.save()
    return redirect('/dashboard')

def myjob_cancel(request, id):
    job = UserJob.objects.get(id = id)
    job.delete()
    return redirect('/dashboard')

def myjob_view_job(request, id):
    if request.session['logged_in']:
        request.session['login_fail'] = ""
        return render(request, 'handyhelper/view_job.html', {'job': UserJob.objects.get(id = id)})
    else:
        request.session['login_fail'] = "You are not logged in. Please sign in here or create an account."
    return redirect('/')