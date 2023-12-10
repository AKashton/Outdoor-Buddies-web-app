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

from django.core.mail import send_mail
from django.http import HttpResponse

def send_test_email(request):
    subject = 'Hello from Outdoor Buddies'
    message = 'This is a test email from your Django application.'
    email_from = 'arcurry@alaska.edu'
    recipient_list = ['arcurry@alaska.edu']  # Replace with your email address for testing
    
    send_mail(subject, message, email_from, recipient_list)
    
    return HttpResponse("Test email sent!")


'''
handling profile picture uploads

def some_profile_update_view(request):
    if request.method == 'POST':
        # Assuming you have a form for profile data
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            # Redirect or inform of success
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'some_template.html', {'form': form})

this is for the form to upload a photo to
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <!-- Render form fields here -->
    <button type="submit">Submit</button>
</form>

'''