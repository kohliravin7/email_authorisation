from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(null=True, max_length=50)
    expiry_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.first_name + self.user.last_name



