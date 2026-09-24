from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from backend.models import Vehicle


@login_required
def dashboard(request):
    vehicles = Vehicle.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total_predictions = vehicles.count()
    latest_vehicle = vehicles.first()

    return render(
        request,
        "home/dashboard.html",
        {
            "total_predictions": total_predictions,
            "latest_vehicle": latest_vehicle,
        },
    )