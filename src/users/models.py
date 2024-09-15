from django.db import models
from django.contrib.auth.models import AbstractUser
from general.choices import UserRoleType, UserGenderType
from general.models import BaseModel


class User(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=24, null=True, blank=True)
    last_name = models.CharField(max_length=24, null=True, blank=True)
    username = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=13, null=False, unique=True)
    role = models.CharField(
        max_length=24, default=UserRoleType.user.value,
        choices=UserRoleType.choices)
    gender = models.CharField(max_length=14, choices=UserGenderType.choices, default=UserGenderType.non_binary.value)
    date_of_birth = models.DateField(null=True)
