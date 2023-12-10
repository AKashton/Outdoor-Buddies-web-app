from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

#tags include biking and hiking
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#this model is the basis for creating posts for adventures
class Adventure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='adventure_pics')
    description = models.TextField()
    max_participants = models.IntegerField()
    location = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    event_datetime = models.DateTimeField()
    status = models.CharField(max_length=100)
    likes = models.ManyToManyField(User, related_name='liked_adventures', blank=True)

    def __str__(self):
        return self.description
    
    def total_likes(self):
        return self.likes.count()

# comments on adventures
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

#users can like adventures
class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)

#model to save participants
class AdventureParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)

#profile setup
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True)
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=255, blank=True)

    def profile_photo_url(self):
        if self.profile_photo and hasattr(self.profile_photo, 'url'):
            return self.profile_photo.url
        else:
            return staticfiles_storage.url('outdoorbuddies/images/default.jpg')  # Path to the default image

    def __str__(self):
        return f'{self.user.username} Profile'
    
#signals to instance a new profile for a new user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
#saves the profile instance
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()