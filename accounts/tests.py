from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsSmokeTests(TestCase):
    def test_signup_get(self):
        resp = self.client.get(reverse("accounts:signup"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "signup")

    def test_signup_post_and_login(self):
        resp = self.client.post(reverse("accounts:signup"), {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "StrongPassw0rd!",
            "password2": "StrongPassw0rd!",
        }, follow=True)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["user"].is_authenticated)

    def test_login_invalid(self):
        resp = self.client.post(reverse("accounts:login"), {
            "username": "nonexistent",
            "password": "whatever"
        })
        self.assertContains(resp, "اسم المستخدم أو كلمة المرور غير صحيحة", status_code=200)

    def test_logout(self):
        user = User.objects.create_user(username="u", password="p")
        self.client.login(username="u", password="p")
        resp = self.client.get(reverse("accounts:logout"), follow=True)
        self.assertFalse(resp.context["user"].is_authenticated)
