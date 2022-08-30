from django.db import models


# Create your models here.
class SubscribedUser(models.Model):
    email = models.EmailField()

    def __str__(self):
        return str(self.email)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['email', ], name='unique_subscription')
        ]
