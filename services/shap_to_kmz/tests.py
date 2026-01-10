from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class ShapToKmzViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("shap_to_kmz:form")

    def test_get_form(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Convert Shapefile Archive to KML")

    def test_post_invalid_extension(self):
        fake = SimpleUploadedFile("not_archive.txt", b"dummy", content_type="text/plain")
        resp = self.client.post(self.url, {"file": fake}, follow=True)
        self.assertContains(resp, "Only .zip or .rar archives are allowed.")
