from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Adventure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='adventure_pics')
    description = models.TextField()
    max_participants = models.IntegerField()
    location = models.CharField(max_length=255)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    event_datetime = models.DateTimeField()
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.description

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class UserLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)

class AdventureParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
