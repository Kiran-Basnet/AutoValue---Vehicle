from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

        fields = [
            "brand",
            "model",
            "year",
            "mileage",
            "engine_capacity",
            "fuel_type",
            "transmission",
            "condition",
            "location",
        ]

        widgets = {
            "brand": forms.TextInput(
                attrs={"placeholder": "Toyota"}
            ),
            "model": forms.TextInput(
                attrs={"placeholder": "Corolla"}
            ),
            "year": forms.NumberInput(
                attrs={"placeholder": "2020"}
            ),
            "mileage": forms.NumberInput(
                attrs={"placeholder": "45000"}
            ),
            "engine_capacity": forms.NumberInput(
                attrs={"placeholder": "1500"}
            ),
            "location": forms.TextInput(
                attrs={"placeholder": "Kathmandu"}
            ),
        }

    def clean_brand(self):
        brand = self.cleaned_data["brand"].strip()

        if not brand:
            raise forms.ValidationError(
                "Brand is required."
            )

        return brand

    def clean_model(self):
        model = self.cleaned_data["model"].strip()

        if not model:
            raise forms.ValidationError(
                "Model is required."
            )

        return model

    def clean_year(self):
        year = self.cleaned_data["year"]

        if year < 1900:
            raise forms.ValidationError(
                "Please enter a valid vehicle year."
            )

        if year > 2030:
            raise forms.ValidationError(
                "Vehicle year cannot be greater than 2030."
            )

        return year

    def clean_mileage(self):
        mileage = self.cleaned_data["mileage"]

        if mileage < 0:
            raise forms.ValidationError(
                "Mileage cannot be negative."
            )

        return mileage

    def clean_engine_capacity(self):
        engine_capacity = self.cleaned_data["engine_capacity"]

        if engine_capacity <= 0:
            raise forms.ValidationError(
                "Engine capacity must be greater than 0."
            )

        return engine_capacity

    def clean_location(self):
        location = self.cleaned_data["location"].strip()

        if not location:
            raise forms.ValidationError(
                "Location is required."
            )

        return location