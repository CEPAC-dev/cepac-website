from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class PdfToWordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("pdf_to_word:form")

    def test_get_form(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Convert PDF to Word")

    def test_post_invalid_extension(self):
        fake = SimpleUploadedFile("not_pdf.txt", b"dummy", content_type="text/plain")
        resp = self.client.post(self.url, {"file": fake}, follow=True)
        self.assertContains(resp, "Only PDF files are allowed.")

    def test_post_valid_pdf(self):
        # minimal valid PDF header so converter might fail but we can test upload flow
        pdf_content = b"%PDF-1.4\n%âãÏÓ\n"
        fake_pdf = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")
        resp = self.client.post(self.url, {"file": fake_pdf}, follow=True)
        # Either conversion error or success, but we expect the view responds without 500
        self.assertIn(resp.status_code, (200, 302))
