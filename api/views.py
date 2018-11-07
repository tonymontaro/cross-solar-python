"""API Views."""
from collections import defaultdict

from rest_framework import viewsets, status
from rest_framework.views import APIView, Response
from .models import Panel, OneHourElectricity
from .serializers import PanelSerializer, OneHourElectricitySerializer


class PanelViewSet(viewsets.ModelViewSet):
    """Panel View Set."""

    queryset = Panel.objects.all()
    serializer_class = PanelSerializer


class HourAnalyticsView(APIView):
    """Hourly Analytics."""

    serializer_class = OneHourElectricitySerializer

    def get(self, request, panelid):
        """Retrieve Hourly Analytics for a Panel."""
        panelid = int(self.kwargs.get('panelid', 0))
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        items = OneHourElectricitySerializer(queryset, many=True)
        return Response(items.data)

    def post(self, request, panelid):
        """Create Hourly Report for a Panel."""
        serializer = OneHourElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DayAnalyticsView(APIView):
    """Daily Analytics."""

    def get(self, request, panelid):
        """Generate Daily Analytics."""
        daily_report = defaultdict(list)
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        for item in queryset:
            daily_report[item.date_time.strftime('%Y-%m-%d')].append(
                item.kilo_watt)

        result = []
        for day, values in daily_report.items():
            kilo_watt_sum = sum(values)
            result.append({
                'date_time': day,
                'sum': kilo_watt_sum,
                'average': kilo_watt_sum / len(values),
                'maximum': max(values),
                'minimum': min(values),
            })
        return Response(sorted(result, key=lambda x: x['date_time']))
