from django.db import models
from accounts.models import User, UserProfile
from vendor.utils import send_notification

# Create your models here.

class Vendor(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
  user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="user_profile")
  vendor_name = models.CharField(max_length=50)
  vendor_slug = models.SlugField(max_length=100, unique=True)
  vendor_license = models.ImageField(upload_to='vendor/license')
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.vendor_name
  
  def save(self, *args, **kwargs):
    if self.pk is not None:
      orig = Vendor.objects.get(pk=self.pk)
      if orig.is_approved != self.is_approved:
        context = {
          'user': self.user,
          'is_approved': self.is_approved
        }
        template = 'vendor/emails/admin_vendor_approval.html'
        if self.is_approved == True:
          mail_subject = 'Congratulations! Your restaurant has been approved.'
          
          send_notification(template, mail_subject, context)
        else:
          mail_subject = 'We are sorry! Your restaurant has been disapproved.'
          send_notification(template, mail_subject, context)
    return super(Vendor, self).save(*args, **kwargs)