from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ContactForm, AdventureForm, CommentForm, ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Adventure, Comment
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

#register a new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # can add logic here to automatically log in the user
            return redirect('outdoorbuddies/index.html')
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

#for each aventure 
def adventure_detail(request, adventure_id):
    adventure = get_object_or_404(Adventure, id=adventure_id)
    comments = Comment.objects.filter(adventure=adventure).order_by('-timestamp')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.adventure = adventure
            comment.save()
            return redirect('adventure_detail', adventure_id=adventure_id)
    else:
        comment_form = CommentForm()

    return render(request, 'outdoorbuddies/adventure_detail.html', {'adventure': adventure, 'comments': comments, 'comment_form': comment_form})

#---------------------------------- login required ----------------------------------------------------

#adventure form creation
@login_required
def create_adventure(request):
    if request.method == 'POST':
        form = AdventureForm(request.POST, request.FILES)
        if form.is_valid():
            adventure = form.save(commit=False)
            adventure.user = request.user  # Set the current user as the creator of the adventure
            adventure.save()
            return redirect('index')  # Redirect to a success page or detail view of the adventure
    else:
        form = AdventureForm()

    return render(request, 'outdoorbuddies/create_adventure.html', {'form': form})

# liking an adventure
@login_required
def liked_adventures(request):
    user = request.user
    adventures = user.liked_adventures.all()
    return render(request, 'outdoorbuddies/liked_adventures.html', {'adventures': adventures})

@login_required
def like_adventure(request, adventure_id):
    adventure = Adventure.objects.get(id=adventure_id)
    if request.user in adventure.likes.all():
        adventure.likes.remove(request.user)
    else:
        adventure.likes.add(request.user)
    return HttpResponseRedirect(reverse('adventure-detail', args=[adventure_id]))

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    
    user_adventures = Adventure.objects.filter(user=request.user)
    return render(request, 'outdoorbuddies/profile.html', {'profile_form': profile_form, 'adventures': user_adventures})

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