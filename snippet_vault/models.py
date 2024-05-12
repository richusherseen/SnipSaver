from django.db import models
from django.contrib.auth.models import User

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True

class Tag(Base):
    title = models.CharField(max_length=100)
    
    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]

    def __str__(self):
        return self.title

class Snippet(Base):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

