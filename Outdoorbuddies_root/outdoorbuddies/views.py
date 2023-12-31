from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, ContactForm, AdventureForm, CommentForm, ProfileForm
from django.http import HttpResponse, HttpResponseRedirect
from .models import Adventure, Comment, AdventureParticipants, Profile, User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

#searching for users and adventures
def search_results(request):
    query = request.GET.get('q', '')
    profiles = Profile.objects.filter(
        Q(user__username__icontains=query)
    )
    adventures = Adventure.objects.filter(
        Q(description__icontains=query) | 
        Q(user__username__icontains=query) |
        Q(location__icontains=query)  # Add location-based filtering
    )
    return render(request, 'outdoorbuddies/search_results.html', {
        'profiles': profiles, 
        'adventures': adventures,
        'query': query
    })

#register a new user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # can add logic here to automatically log in the user
            return redirect('index')
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

#displays a user profile
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    # Get adventures posted by the user
    posted_adventures = Adventure.objects.filter(user=user)

    # Get adventures where the user is a participant
    participating_adventures = Adventure.objects.filter(adventureparticipants__user=user)

    # Combine both QuerySets into a single list, avoiding duplicates
    user_adventures = (posted_adventures | participating_adventures).distinct()

    return render(request, 'outdoorbuddies/user_profile.html', {
        'profile_user': user,
        'profile': profile,
        'user_adventures': user_adventures
    })

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
    participants = AdventureParticipants.objects.filter(adventure=adventure)
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

    return render(request, 'outdoorbuddies/adventure_detail.html', {'adventure': adventure, 'participants' : participants, 'comments': comments, 'comment_form': comment_form})

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
            AdventureParticipants.objects.create(user=request.user, adventure=adventure, is_host=True)
            return redirect('adventure_detail', adventure.id)
    else:
        form = AdventureForm()

    return render(request, 'outdoorbuddies/create_adventure.html', {'form': form})

#remove adventure
@login_required
def delete_adventure(request, adventure_id):
    adventure = get_object_or_404(Adventure, id=adventure_id)

    # Check if the request user is the host
    if adventure.user == request.user:
        adventure.delete()
        messages.success(request, 'Adventure deleted successfully.')
        return HttpResponseRedirect(reverse('index'))  # Redirect to the home page
    else:
        messages.error(request, 'You do not have permission to delete this adventure.')
        return HttpResponseRedirect(reverse('adventure_detail', args=[adventure_id]))
    
# liking an adventure
@login_required
def liked_adventures(request):
    user = request.user
    adventures = user.liked_adventures.all()
    return render(request, 'outdoorbuddies/liked_adventures.html', {'adventures': adventures})

@login_required
def like_adventure(request, adventure_id):
    adventure = get_object_or_404(Adventure, id=adventure_id)
    if request.user in adventure.likes.all():
        adventure.likes.remove(request.user)
    else:
        adventure.likes.add(request.user)
    return redirect(reverse('adventure_detail', args=[adventure_id]))

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

@login_required
def join_adventure(request, adventure_id):
    adventure = get_object_or_404(Adventure, id=adventure_id)
    if not AdventureParticipants.objects.filter(user=request.user, adventure=adventure).exists():
        AdventureParticipants.objects.create(user=request.user, adventure=adventure)
    return redirect('adventure_detail', adventure_id=adventure.id)