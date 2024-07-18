from django.db import models

from django.contrib import messages
from django_ckeditor_5.fields import CKEditor5Field
from taggit.managers import TaggableManager
from django.db.models import Count, Q
from accounts.models import CustomUser

 
# Create your models here.
class Topic(models.Model):
    Category_CHOICES = (
    ('Topik','Topik'),
    ('KIIP', 'KIIP'),
    ('Daily','Daily'),
    ('Other','Other'))

    author = models.ForeignKey(CustomUser, related_name='topics',on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = CKEditor5Field('Text', config_name='extends')
    
    hashtag = TaggableManager(blank=True)
    category = models.CharField(choices=Category_CHOICES, default='Topik', max_length=15)
    pub_date = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.topic_title 
    
    def save(self, *args, **kwargs):
        # Call the original save method
        super().save(*args, **kwargs)
        
        # Check if there are any tags
        if not self.hashtag.all().exists():
            # If no tags, add a default tag
            self.hashtag.add('general')
