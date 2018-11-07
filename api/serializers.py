"""Serializer Module."""
from rest_framework import serializers
from .models import Panel, OneHourElectricity


class PanelSerializer(serializers.ModelSerializer):
    """Panel Serializer."""

    class Meta:
        """Serializer Meta."""

        model = Panel
        fields = ('id', 'brand', 'serial', 'latitude', 'longitude')


class OneHourElectricitySerializer(serializers.ModelSerializer):
    """Hourly Report Serializer."""

    class Meta:
        """Serializer Meta."""

        panel = serializers.PrimaryKeyRelatedField(
            queryset=Panel.objects.all())
        model = OneHourElectricity
        fields = ('id', 'panel', 'kilo_watt', 'date_time')
