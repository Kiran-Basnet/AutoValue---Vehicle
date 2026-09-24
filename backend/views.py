import requests
import pandas as pd

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

from .forms import VehicleForm
from .models import Vehicle

from django.contrib.auth.decorators import login_required


FASTAPI_URL = "http://127.0.0.1:8001/predict"

@login_required
def valuation(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)

        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.user = request.user

            data = {
                "brand": vehicle.brand,
                "model": vehicle.model,
                "year": vehicle.year,
                "mileage": vehicle.mileage,
                "engine_capacity": vehicle.engine_capacity,
                "fuel_type": vehicle.fuel_type,
                "transmission": vehicle.transmission,
                "condition": vehicle.condition,
                "location": vehicle.location,
            }

            try:
                response = requests.post(
                    FASTAPI_URL,
                    json=data,
                    timeout=10
                )

                response.raise_for_status()

                prediction_data = response.json()

                if "predicted_price" not in prediction_data:
                    raise ValueError("Prediction value missing.")

                predicted_price = prediction_data["predicted_price"]

                vehicle.predicted_price = predicted_price

                # Save only after successful prediction
                vehicle.save()

            except requests.exceptions.RequestException as e:
                print("FASTAPI ERROR:", e)
                return render(
                    request,
                    "backend/valuation.html",
                    {
                        "form": form,
                        "api_error": (
                            "Prediction service is currently unavailable. "
                            "Please make sure the FastAPI server is running."
                        ),
                    },
                )

            except (ValueError, KeyError, TypeError):
                return render(
                    request,
                    "backend/valuation.html",
                    {
                        "form": form,
                        "api_error": (
                            "The prediction service returned an invalid result."
                        ),
                    },
                )

            return render(
                request,
                "backend/result.html",
                {
                    "vehicle": vehicle,
                    "predicted_price": predicted_price,
                },
            )

    else:
        form = VehicleForm()

    return render(
        request,
        "backend/valuation.html",
        {
            "form": form,
        },
    )


@login_required
def history(request):
    vehicles = Vehicle.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "backend/history.html",
        {
            "vehicles": vehicles,
        },
    )

def vehicle_suggestions(request):
    field = request.GET.get("field", "")
    query = request.GET.get("q", "").strip().lower()
    brand = request.GET.get("brand", "").strip().lower()

    dataset_path = settings.BASE_DIR / "Dataset.csv"

    try:
        df = pd.read_csv(dataset_path)
    except Exception:
        return JsonResponse(
            {"error": "Dataset could not be loaded."},
            status=500
        )

    # -------------------------
    # BRAND
    # -------------------------
    if field == "brand":
        values = (
            df["brand"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        suggestions = [
            value for value in values
            if query in value.lower()
        ]

        return JsonResponse({
            "suggestions": sorted(suggestions)[:10]
        })

    # -------------------------
    # MODEL
    # -------------------------
    if field == "model":
        data = df.copy()

        if brand:
            data = data[
                data["brand"]
                .astype(str)
                .str.lower()
                .str.strip()
                == brand
            ]

        values = (
            data["model"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        suggestions = [
            value for value in values
            if query in value.lower()
        ]

        return JsonResponse({
            "suggestions": sorted(suggestions)[:10]
        })

    # -------------------------
    # FUEL TYPE
    # -------------------------
    if field == "fuel_type":
        values = (
            df["Fuel type:"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        suggestions = [
            value for value in values
            if query in value.lower()
        ]

        return JsonResponse({
            "suggestions": sorted(suggestions)[:10]
        })

    # -------------------------
    # TRANSMISSION
    # -------------------------
    if field == "transmission":
        values = (
            df["transmission"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        suggestions = [
            value for value in values
            if query in value.lower()
        ]

        return JsonResponse({
            "suggestions": sorted(suggestions)[:10]
        })

    # -------------------------
    # CONDITION
    # -------------------------
    if field == "condition":
        values = (
            df["condition"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
        )

        suggestions = [
            value for value in values
            if query in value.lower()
        ]

        return JsonResponse({
            "suggestions": sorted(suggestions)[:10]
        })

    # -------------------------
    # LOCATION
    # -------------------------
    if field == "location":

        # The dataset's area column sometimes contains
        # newline + view count, so keep only the first part.
        areas = (
            df["area"]
            .dropna()
            .astype(str)
            .str.split("\n")
            .str[0]
            .str.strip()
        )

        subareas = (
            df["subarea"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        values = pd.concat([areas, subareas]).drop_duplicates()

        suggestions = [
            value for value in values
            if query in value.lower()
        ]

        return JsonResponse({
            "suggestions": sorted(suggestions)[:10]
        })

    # -------------------------
    # NUMERIC RANGES
    # -------------------------
    if field == "year":

        values = pd.to_numeric(
            df["man_year"],
            errors="coerce"
        ).dropna()

        return JsonResponse({
            "min": int(values.min()),
            "max": int(values.max())
        })

    if field == "mileage":

        values = (
            df["km_run"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+(?:\.\d+)?)")[0]
        )

        values = pd.to_numeric(
            values,
            errors="coerce"
        ).dropna()

        return JsonResponse({
            "min": int(values.min()),
            "max": int(values.max())
        })

    if field == "engine_capacity":

        values = (
            df["engine_capacity"]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.extract(r"(\d+(?:\.\d+)?)")[0]
        )

        values = pd.to_numeric(
            values,
            errors="coerce"
        ).dropna()

        return JsonResponse({
            "min": int(values.min()),
            "max": int(values.max())
        })

    return JsonResponse({
        "error": "Unknown field."
    }, status=400)