from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="vehicles",
    null=True,
    blank=True
    )

    FUEL_CHOICES = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Electric", "Electric"),
        ("Hybrid", "Hybrid"),
    ]

    TRANSMISSION_CHOICES = [
        ("Manual", "Manual"),
        ("Automatic", "Automatic"),
    ]

    CONDITION_CHOICES = [
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Poor", "Poor"),
    ]

    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField()
    engine_capacity = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES
    )
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    predicted_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"