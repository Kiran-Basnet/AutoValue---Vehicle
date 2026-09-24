from django.contrib import admin
from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "model",
        "year",
        "mileage",
        "fuel_type",
        "transmission",
        "condition",
        "location",
    )

    list_filter = (
        "fuel_type",
        "transmission",
        "condition",
    )

    search_fields = (
        "brand",
        "model",
        "location",
    )