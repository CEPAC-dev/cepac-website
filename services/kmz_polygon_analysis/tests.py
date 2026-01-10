from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import os

class KMZPolygonAnalysisViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("kmz_polygon_analysis:form")

    def test_get_form(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "KMZ / KML Polygon Analysis")

    def test_post_invalid_extension(self):
        fake = SimpleUploadedFile("test.txt", b"not a kmz", content_type="text/plain")
        resp = self.client.post(self.url, {"file": fake}, follow=True)
        self.assertContains(resp, "Please upload a .kmz file.")

    # Note: A full integration test would require a real minimal .kmz with a KML inside.
