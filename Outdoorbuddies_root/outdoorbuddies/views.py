from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # can add logic here to automatically log in the user
            return redirect('some-view')
    else:
        form = UserRegisterForm()
    return render(request, 'outdoorbuddies/register.html', {'form': form})

def index(request):
    return HttpResponse("Hello, world. You're at my website.")