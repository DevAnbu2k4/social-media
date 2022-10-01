from ctypes.wintypes import SIZE
from distutils.command.upload import upload
from logging import lastResort
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from PIL import Image
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import os

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    recipent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    body = models.TextField(max_length=1000, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, body):
        sender_message = Message(
            user = from_user,
            sender = from_user,
            recipent = to_user,
            body = body,
            is_read = True)
        sender_message.save()

        recipent_message = Message(
            user = to_user,
            sender = from_user,
            body = body,
            recipent = from_user)
        recipent_message.save()

        return sender_message

    def get_message(user):
        users = []
        messages = Message.objects.filter(user=user).values('recipent').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user': User.objects.get(pk=message['recipent']),
                'last': message['last'],
                'unread': Message.objects.filter(user=user, recipent__pk=message['recipent'], is_read=False).count()
            })
        return users


class UserProfile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
        profile_Picture = models.ImageField(upload_to = 'profile_Picture', blank=True, null=True,verbose_name='Picture')
        Bio = models.CharField(max_length=50, null=True)

        def save(self,force_insert=False, force_update=False, using=None,*args, **kwargs):
            if self.profile_Picture:
                image = self.profile_Picture
                if image.size > 0.3*1024*1024: #if size greater than 300kb then it will send to compress image function
                    self.profile_Picture = compress_image(image)
            super(UserProfile, self).save(*args, **kwargs)


        def __str__(self):
		        return self.user.username
    
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

from django.core.files import File
from io import BytesIO
from PIL import Image

def compress_image(image):
    im = Image.open(image)
    if im.mode != 'RGB':
        im = im.convert('RGB')
    im_io = BytesIO()
    im.save(im_io, 'jpeg', quality=70,optimize=True)
    new_image = File(im_io, name=image.name)
    return new_image