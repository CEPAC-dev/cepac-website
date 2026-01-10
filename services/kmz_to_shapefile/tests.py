from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class KmzToShapefileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("kmz_to_shapefile:form")

    def test_get_form(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Convert KMZ to Shapefile")

    def test_post_invalid_extension(self):
        fake = SimpleUploadedFile("not_kmz.txt", b"dummy content", content_type="text/plain")
        resp = self.client.post(self.url, {"file": fake}, follow=True)
        self.assertContains(resp, "Please upload a .kmz file.")
