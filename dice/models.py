from django.core.exceptions import ValidationError
from django.db import models
import re


def validate_name(value):
    if not re.match(r"^[0-9a-zA-Z,+\- ]+$", value):
        raise ValidationError("Name must be alphanumeric")


def validate_throws(value):
    if not re.match(r"^[0-9, ]+$", value):
        raise ValidationError(
            "Throw must be a single number or match the pattern '{int}, {int}, ...}'"
        )


def validate_modifier(value):
    if not re.match(r"^(str|int|dex|con|wis|cha)\([+-]\d+\)$", value):
        raise ValidationError("Modifier must match the pattern '{mod}({+/-}{int})'")


class Dice(models.Model):
    name = models.CharField(max_length=255, validators=[validate_name])
    dice = models.IntegerField()
    sides = models.IntegerField()
    throws = models.CharField(max_length=255, validators=[validate_throws])
    sum = models.IntegerField()
    modifier = models.CharField(
        max_length=255,
        default="",
        blank=True,
        validators=[validate_modifier],
    )
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
