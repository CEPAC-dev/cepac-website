from django.db import models
from django.contrib.auth.models import User

# Optional: extend user with profile if needed later.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add extra fields here, e.g.:
    # organization = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
