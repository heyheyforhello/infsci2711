import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from simplestore.checkout.models.address import Address


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **kwargs):
        superuser = self.create_user(email, password, **kwargs)
        superuser.is_admin = True
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()

        return superuser


class Profile(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created = models.DateField(auto_now_add=True)
    slug = models.SlugField(blank=False)
    updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    website = models.URLField(blank=True)
    about = models.TextField(blank=True)

    aid = models.ForeignKey(Address,on_delete=models.CASCADE,null=True,blank=True) # to deal with one-to-many relations
    TYPE_CHOICES = (
       ('H', 'Buy_for_home'),
       ('B', 'Buy_for_business'),
    )
    last_name = models.CharField(max_length=100,blank=False)
    first_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(max_length=100)
    kind = models.CharField(max_length=1, choices=TYPE_CHOICES)
    phone = models.CharField(max_length=13, help_text="The format should be like (xxx)xxx-xxxx")

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.email

class Home(models.Model):
    cid = models.OneToOneField(Profile, on_delete=models.CASCADE)
    MARRIAGE_CHOICES = (
       ('Y', 'Is_married'),
       ('N', 'Not_married'),
    )
    marriage_status = models.CharField(max_length=1, choices=MARRIAGE_CHOICES)
    GENDER_CHOICES = (
       ('F', 'Female'),
       ('M', 'Male'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)


class Business(models.Model):
    cid = models.OneToOneField(Profile, on_delete=models.CASCADE)
    bussiness_category = models.CharField(max_length=50) # business category
    gross_anunal_income = models.DecimalField(max_digits=10, decimal_places=2) # company gross annual income
