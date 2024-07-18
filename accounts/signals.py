from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, CustomUser 
from django.contrib.auth.models import User




@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        # This will create a profile if it doesn't exist
        UserProfile.objects.get_or_create(user=instance)
    
    # Always save the profile
    instance.profile.save()