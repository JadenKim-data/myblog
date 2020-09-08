import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class User(AbstractUser):
    class GENDER_CHOICES(models.TextChoices):
        MALE = "M", "남성"
        FEMALE = "F", "여성"

    avatar = models.ImageField(blank=True, upload_to="accounts/avatar/%Y/%m/%d")
    phone_number = models.CharField(
        max_length=13, validators=[RegexValidator(r"^010-[1-9]\d{3}-\d{4}$")],
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES.choices)
    birth_date = models.DateField(auto_now=False, auto_now_add=False, default=datetime.date(1111, 11, 11))

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def avatar_url(self):
        if (self.avatar):
            return self.avatar.url

