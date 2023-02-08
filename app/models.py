from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse
from ckeditor.fields import RichTextField

#
# # Create your models here.
class Class(models.Model):
    subject_field = models.CharField(max_length=10, default="subject")
    catalog_number_field = models.CharField(max_length=10, default="catalog")
    course_number_field = models.CharField(max_length=10, default="course number")
    description_field = models.CharField(max_length=50, default="description", blank=True)
    instructor_field = models.CharField(max_length=50, default="instructor", blank=True)
    def __str__(self):
        return self.subject_field + self.catalog_number_field


class Profile(models.Model):
#https://dev.to/earthcomfy/django-user-profile-3hik -- where I recieved guidance on how to create the profile
    Ages = (

        ('First Year', 'First Year'),
        ('Second Year', 'Second Year'),
        ('Third Year', 'Third Year'),
        ('Fourth Year', 'Fourth Year'),
        ('Graduate Student','Graduate Student'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Age = models.CharField(max_length=150, choices=Ages)
    # Enrolled_Courses = models.TextField()
    Enrolled_Courses = models.ManyToManyField(Class, blank=True)
    Major = models.TextField()
    Bio = models.TextField(blank=True)

    Following = models.ManyToManyField('self', blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    #def get_friends(self):
        #return self.friends.all()

    #def get_friends_no(self):
        #return self.friends.all().count()
    def __str__(self):
        return str(self.user)


class StudySessionModel (models.Model):
    title = models.CharField(max_length = 200)
    #text = models.TextField()
    text = RichTextField(blank = True, null=True)
    class_name = models.CharField(max_length = 200, choices =[])
    start_time = models.DateTimeField()
    duration = models.CharField(max_length = 10)
    address = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    enroll = models.ManyToManyField(User,related_name='user_enroll')

    def __str__(self):
        return self.title+ ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('list')


class Discussions(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length = 200)
    post = models.ForeignKey(StudySessionModel, on_delete=models.CASCADE, default='')