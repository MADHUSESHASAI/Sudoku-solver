from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html')

def loginpage(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.extend(errors)
            messages.error(request, " ".join(error_messages))
    else:
        form = AuthenticationForm()
    return render(request, 'loginpage.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/loginpage')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                error_messages.extend(errors)
            messages.error(request, " ".join(error_messages))
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def temp1(request):#madhu
    values=['?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',
    '?','?','?','?','?','?','?','?','?',]
    if request.method=='POST':
        data=request.POST
        
        for i in range(1,82):
            values[i-1]=data[str(i)]
        print(values)
       
    return render(request,'1.html',context={'list':values} )
