from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from PIL import Image
from django.views.generic import RedirectView

# # Create your models here.
# class Signup(models.Model):
#     user=models.OneToOneField(User,on_delete=models.DO_NOTHING)
#     def __str__(self):
#         return self.user
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default="default.jpg")

    # default = 'path/to/my/default/image.jpg'
    def __str__(self):
        return f'{self.user.username} Profile'

    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    post_save.connect(create_profile,sender=User)
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    # def save(self):
    #     super().save()
    #     img = Image.open(self.image.path)
    #     if img.height > 300 and img.width > 300:
    #         outputsize = (300, 300)
    #         img.thumbnail(outputsize)
    #         img.save(self.image.path)
