from django.db import models


# Create your models here.
class SubscribedUser(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return str(self.email)
