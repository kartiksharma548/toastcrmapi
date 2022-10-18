from datetime import datetime
from email.policy import default
from enum import unique
from pickle import FALSE, TRUE
from django.utils.translation import gettext_lazy  as _
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser,BaseUserManager,PermissionsMixin
from django_resized import ResizedImageField
# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self,email,password,first_name,last_name,mobile,**extra_fields):
        if not email:
            raise ValueError("Email is required.")
        if not password:
            raise ValueError("Password is required")

        user=self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name,mobile=mobile,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self,email,password,first_name,last_name,mobile,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(email,password,first_name,last_name,mobile,**extra_fields)
    
    def create_superuser(self,email,password,first_name,last_name,mobile,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_superuser',True)

        return self._create_user(email,password,first_name,last_name,mobile,**extra_fields)

class User(AbstractUser,PermissionsMixin):
    
    email = models.EmailField(db_index=True, unique=True,max_length=254)
    first_name=models.CharField(max_length=240)
    last_name=models.CharField(max_length=240)
    mobile=models.CharField(max_length=240)

    is_staff=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=True)

    picture=ResizedImageField(size=[210, 240],upload_to="images",default="")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile', 'first_name', 'last_name']
   

    objects=CustomUserManager()
    def __str__(self):
        return "{}".format(self.email)


class Team(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Employee(models.Model):
    first_name = models.CharField(max_length=64)

    last_name = models.CharField(max_length=64)

    current_role = models.CharField(max_length=64)  # "coder"

    # "coder, developer, janator" (seperator: ,)
    past_roles = models.CharField(max_length=512)

    teams = models.ManyToManyField(Team, related_name="employees", blank=True)

    joining_date = models.DateTimeField(null=True, blank=True)

    def team(self):
        return ",".join([str(e) for e in self.teams.all()])


class Status(models.Model):

    status_id = models.AutoField(primary_key=TRUE, unique=True)

    status_name = models.CharField(max_length=64, default="")

    status_id_name = models.CharField(max_length=64, default="")

    status_forecolor = models.CharField(max_length=64, default="")

    status_backcolor = models.CharField(max_length=64, default="")

    def __str__(self):
        return self.status_name


class Sub_Status(models.Model):

    sub_status_id = models.AutoField(primary_key=True)
    sub_status_name = models.CharField(max_length=64, default="")
    statusForCancellation = models.BooleanField(default=False)
    status = models.ForeignKey(
        Status, default=1, to_field="status_id", on_delete=models.CASCADE, related_name='status_field')

    def __str__(self):
        return self.sub_status_name


class Lead(models.Model):

    lead_id = models.AutoField(primary_key=TRUE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)

    first_name = models.CharField(max_length=64)

    last_name = models.CharField(max_length=64)

    dob = models.DateField(null=True, blank=True)

    phone_number = models.CharField(max_length=10)

    city = models.CharField(max_length=64)

    state = models.CharField(max_length=64)
    zip = models.CharField(max_length=64)
    address1 = models.TextField(max_length=250)
    address2 = models.TextField(max_length=250)
    substatus = models.ForeignKey(
        Sub_Status, default=1, to_field="sub_status_id", on_delete=models.CASCADE)
    status_changedOn = models.DateTimeField(default=datetime.now())

    @property
    def full_name(self):
        return self.first_name+' '+self.last_name


class Note(models.Model):
    note_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    note = models.TextField()
    dateTime = models.DateTimeField(default=datetime.now())
    lead = models.ForeignKey(
        Lead, default=None, to_field="lead_id", on_delete=models.CASCADE)


class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    schedule_dateTime = models.DateTimeField(default=datetime.now())
    schedule_updatedateTime = models.DateTimeField(default=datetime.now())

    isCompleted = models.BooleanField(default=False)
    isCancelled = models.BooleanField(default=False)
    added_at = models.DateTimeField(default=datetime.now())
    alarm = models.IntegerField()
    location = models.CharField(max_length=255)
    durationHr = models.IntegerField()
    durationMin = models.IntegerField()
    lead = models.ForeignKey(
        Lead, default=None, to_field="lead_id", on_delete=models.CASCADE)


class AllowedStatus(models.Model):
    current_status = models.ForeignKey(
        Sub_Status, default=1, to_field="sub_status_id", on_delete=models.CASCADE, related_name="current_status")
    allowed_statuses = models.ManyToManyField(
        Sub_Status, related_name="allowed_status")
