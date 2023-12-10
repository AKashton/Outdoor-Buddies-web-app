from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ContactForm
from django.http import HttpResponse
from .models import Adventure
from django.core.mail import send_mail
from django.contrib import messages
#register a new user
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
    # Fetch all adventure postings ordered by most recent
    adventures = Adventure.objects.all().order_by('-event_datetime')
    return render(request, 'outdoorbuddies/index.html', {'adventures': adventures})

#about us page used to describe outdoorbuddies
def about(request):
    return render(request, 'outdoorbuddies/about.html')

#contact us view

#test view to ensure email is working. 
def send_test_email(request):
    subject = 'Hello from Outdoor Buddies'
    message = 'This is a test email from your Django application.'
    email_from = 'arcurry@alaska.edu'
    recipient_list = ['arcurry@alaska.edu']  # Replace with your email address for testing
    
    send_mail(subject, message, email_from, recipient_list)
    
    return HttpResponse("Test email sent!")

#contact us page view
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']
            message = form.cleaned_data['message']

             # Compose the email message
            full_message = f"Sent by: {name}, Email: {sender_email}\n\n{message}"
            send_mail(
                subject=f'Message from {name}',  # subject
                message=full_message,  # message
                from_email='arcurry@alaska.edu',  # Use your default FROM email in Django settings
                recipient_list=['arcurry@alaska.edu'],  # to email
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to a success page
    else:
        form = ContactForm()

    return render(request, 'outdoorbuddies/contact.html', {'form': form})
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