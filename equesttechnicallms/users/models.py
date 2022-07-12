from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Default user for EquesttechnicalLMS."""
    phone = models.CharField(max_length=15)
    avatar = models.ImageField(null=True, default="avatar.svg")
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)
    bio = models.TextField(null=True)

    #: First and last name do not cover name patterns around the globe
    # name = CharField(_("Name of User"), blank=True, max_length=255)
    # first_name = None  # type: ignore
    # last_name = None  # type: ignore

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


