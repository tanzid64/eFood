from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
  if created:
    # Create the user profile on usercreation
    user_profile = UserProfile.objects.create(user=instance)
    user_profile.save()
  else:
    try:
      # Update user profile if exists
      profile = UserProfile.objects.get(user=instance)
      profile.save()
    except:
      # Create the user profile if not exists
      user_profile = UserProfile.objects.create(user=instance)
      user_profile.save()