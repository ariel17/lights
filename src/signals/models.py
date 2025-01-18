from django.contrib.auth.models import User
from django.db import models


class Signal(models.Model):
    name = models.CharField(max_length=50, help_text="Name; has to be unique.", unique=True)
    description = models.TextField(help_text="What is this for?")
    is_enabled = models.BooleanField(default=False, help_text="Is this enabled?")
    author = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, help_text="Creator.")
    created_at = models.TimeField(auto_now_add=True, editable=False, help_text="Date and time of creation.")
    updated_at = models.TimeField(auto_now=True, editable=False, help_text="Date and time of update.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Flag(Signal):
    pass
