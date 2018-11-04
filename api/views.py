from rest_framework import viewsets,status
from rest_framework.views import APIView, Response
from .models import Panel, OneHourElectricity
from .serializers import PanelSerializer, OneHourElectricitySerializer

class PanelViewSet(viewsets.ModelViewSet):
    queryset = Panel.objects.all()
    serializer_class = PanelSerializer

class HourAnalyticsView(APIView):
    serializer_class = OneHourElectricitySerializer
    def get(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        queryset = OneHourElectricity.objects.filter(panel_id=panelid)
        items = OneHourElectricitySerializer(queryset, many=True)
        return Response(items.data)
    def post(self, request, panelid):
        panelid = int(self.kwargs.get('panelid', 0))
        serializer = OneHourElectricitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DayAnalyticsView(APIView):
    def get(self, request, panelid):
        # Please implement this method to return Panel's daily analytics data
        return Response([{
            "date_time": "[date for the day]",
            "sum": 0,
            "average": 0,
            "maximum": 0,
            "minimum": 0
        }])