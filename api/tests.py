from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Panel, OneHourElectricity


class PanelModelTestCase(TestCase):
    def test_create_panel(self):
        panel = Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222",
                                     latitude=90.345678, longitude=120.765543)
        self.assertTrue(isinstance(panel, Panel))
        self.assertEqual(
            panel.__str__(), "Brand: Areva, Serial: AAAA1111BBBB2222")


class OneHourElectricityModelTestCase(TestCase):
    def test_create_report(self):
        panel = Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222",
                                     latitude=90.345678, longitude=120.765543)

        report = OneHourElectricity.objects.create(
            panel=panel, kilo_watt=200, date_time="2018-11-04T03:00:00Z")
        self.assertTrue(isinstance(report, OneHourElectricity))
        self.assertEqual(
            report.__str__(), "Hour: 2018-11-04T03:00:00Z - 200 KiloWatt")


class PanelTestCase(APITestCase):

    def setUp(self):
        self.panel_detail = {
            "brand": "Areva",
            "serial": "AAAA1111BBBB2222",
            "latitude": 80.345678,
            "longitude": 120.765544
        }
        self.create_panel = lambda: self.client.post(
            '/panel/', self.panel_detail, format='json')

    def test_panel_creation(self):
        response = self.create_panel()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")

    def test_panel_listing(self):
        self.create_panel()
        response = self.client.get('/panel/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_panel_get(self):
        self.create_panel()
        response = self.client.get('/panel/1/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["serial"], "AAAA1111BBBB2222")

    def test_invalid_panel_latitude(self):
        self.panel_detail['latitude'] = 90.345678
        response = self.client.post('/panel/', self.panel_detail, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["latitude"][0],
                         "Ensure this value is less than or equal to 90.")

        self.panel_detail['latitude'] = -93.345678
        response = self.client.post('/panel/', self.panel_detail, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["latitude"][0],
                         "Ensure this value is greater than or equal to -90.")

    def test_invalid_panel_longitude(self):
        self.panel_detail['longitude'] = 200.765544
        response = self.client.post('/panel/', self.panel_detail, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["longitude"][0],
                         "Ensure this value is less than or equal to 180.")

        self.panel_detail['longitude'] = -200.765544
        response = self.client.post('/panel/', {
            "serial": "AAAA1111BBBB2222",
            "latitude": 80.345678,
            "longitude": -200.76554
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["longitude"][0],
                         "Ensure this value is greater than or equal to -180.")


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

    def test_invalid_report_creation(self):
        response = self.client.post('/panel/1/analytics/', {
            "panel": 1,
            "kilo_watt": 200,
            "date_time": "2018-11-04"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DayAnalyticsViewTestCase(APITestCase):
    def setUp(self):
        panel = Panel.objects.create(brand="Areva", serial="AAAA1111BBBB2222",
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

        for item in data:
            item['panel'] = panel
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
