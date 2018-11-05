from rest_framework.test import APITestCase
from rest_framework import status
from .models import Panel, OneHourElectricity

class PanelTestCase(APITestCase):
    def setUp(self):
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222",
                             latitude=12.345678, longitude=98.7655432)

    def test_panel_listing(self):
        response = self.client.get('/panel/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_panel_get(self):
        response = self.client.get('/panel/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")


class HourAnalyticsTestCase(APITestCase):
    def setUp(self):
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222",
                             latitude=12.345678, longitude=98.765543)

    def create_report(self):
        return self.client.post('/panel/1/analytics/', {
            "panel": 1,
            "kilo_watt": 200,
            "date_time": "2018-11-04T03:00:00Z"
        }, format='json')

    def test_hourly_report_creation(self):
        response = self.create_report()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["kilo_watt"], 200)

    def test_hourly_report_get(self):
        report = self.create_report()
        self.assertEqual(report.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/panel/1/analytics/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)


class DayAnalyticsViewTestCase(APITestCase):
    def setUp(self):
        Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222",
                             latitude=12.345678, longitude=98.765543)
        data = [
            {
                "kilo_watt": 200,
                "date_time": "2018-11-02T03:00:00Z"
            },
            {
                "kilo_watt": 300,
                "date_time": "2018-11-02T03:00:00Z"
            },
            {
                "kilo_watt": 80,
                "date_time": "2018-11-03T03:00:00Z"
            },
            {
                "kilo_watt": 160,
                "date_time": "2018-11-03T03:00:00Z"
            },
            {
                "kilo_watt": 450,
                "date_time": "2018-11-03T03:00:00Z"
            }
        ]
        panel1 = Panel.objects.get(pk=1)
        for item in data:
            item['panel'] = panel1
            OneHourElectricity.objects.create(**item)

    def test_day_analytics_get(self):
        response = self.client.get('/panel/1/analytics/day', format='json')
        expected = [
            {
                "date_time": "2018-11-02",
                "sum": 500,
                "average": 250.0,
                "maximum": 300,
                "minimum": 200
            },
            {
                "date_time": "2018-11-03",
                "sum": 690,
                "average": 230.0,
                "maximum": 450,
                "minimum": 80
            }
        ]
        self.assertEquals(response.data, expected)
