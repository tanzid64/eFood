import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def allow_only_images_validator(value):
  ext = os.path.splitext(value.name)[1]
  valid_extensions = ['.png', '.jpg', '.jpeg']
  if not ext.lower() in valid_extensions:
    raise ValidationError(_('Please use valid image extension.'))