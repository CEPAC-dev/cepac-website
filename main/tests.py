from django.test import TestCase, Client
from django.urls import reverse

class MainPagesTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        resp = self.client.get(reverse("main:home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "<title", html=False)

    def test_about_page(self):
        resp = self.client.get(reverse("main:about"))
        self.assertEqual(resp.status_code, 200)

    def test_contact_page(self):
        resp = self.client.get(reverse("main:contact"))
        self.assertEqual(resp.status_code, 200)

    def test_portfolio_page(self):
        resp = self.client.get(reverse("main:portfolio"))
        self.assertEqual(resp.status_code, 200)

    def test_service_overview_page(self):
        resp = self.client.get(reverse("main:service_overview"))
        self.assertEqual(resp.status_code, 200)
        # Check that at least one service link appears
        self.assertContains(resp, "Trip Length Distribution")
