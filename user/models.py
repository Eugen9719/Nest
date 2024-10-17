from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    class RoleStatus(models.TextChoices):
        VENDOR = 'V', 'Vendor'
        CUSTOMER = 'C', 'Customer'

    role = models.CharField("Тип пользователя", max_length=1, choices=RoleStatus.choices,
                            default=RoleStatus.CUSTOMER)

    email = models.EmailField("Адрес электронной почты", unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    phone_number = PhoneNumberField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.email}'
