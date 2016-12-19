from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.PositiveIntegerField
    expiry_date = models.DateField

    def __str__(self):
        return self.user.first_name + self.user.last_name



