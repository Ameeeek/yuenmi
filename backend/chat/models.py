from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name 



class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name='messages')
    content = models.TextField()
    anonymous_name = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.anonymous_name}: {self.content[:50]}" 


# Create your models here.
