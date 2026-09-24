from django.urls import path

from .views import valuation, history, vehicle_suggestions

urlpatterns = [
    path("valuation/", valuation, name="valuation"),
    path("history/", history, name="history"),
    path(
        "api/vehicle-suggestions/",
        vehicle_suggestions,
        name="vehicle_suggestions",
    ),
]