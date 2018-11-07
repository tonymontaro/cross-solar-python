"""Models Module."""
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Panel(models.Model):
    """Panel Model."""

    brand = models.CharField(max_length=200, blank=True)
    serial = models.CharField(max_length=200, unique=True)
    latitude = models.DecimalField(
        decimal_places=6, max_digits=8, validators=[
            MaxValueValidator(90),
            MinValueValidator(-90)
        ])
    longitude = models.DecimalField(
        decimal_places=6, max_digits=9, validators=[
            MaxValueValidator(180),
            MinValueValidator(-180)
        ])

    def __str__(self):
        """Model representation."""
        return "Brand: {0}, Serial: {1}".format(self.brand, self.serial)


class OneHourElectricity(models.Model):
    """Hourly Report Model."""

    panel = models.ForeignKey(Panel, on_delete=models.CASCADE)
    kilo_watt = models.BigIntegerField()
    date_time = models.DateTimeField()

    def __str__(self):
        """Model representation."""
        return "Hour: {0} - {1} KiloWatt".format(
            self.date_time, self.kilo_watt)
