from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    cures = models.TextField()
    sideEffects = models.TextField()

    def __str__(self):
        return self.name


class Collection(models.Model):
    medition = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    collected = models.BooleanField(default=False)
    collectedApproved = models.BooleanField(default=False)
    collectedApprovedBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="CollectedApprovedBy", null=True, blank=True
    )

    def __str__(self):
        return self.medition.name


class Profile(models.Model):
    city = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    bioText = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
