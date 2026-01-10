from django.test import TestCase, Client
from django.urls import reverse

class TripLengthFlowTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_initial_get(self):
        resp = self.client.get(reverse("trip_length_distribution:index"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Trip Length Distribution")

    def test_setup_post_invalid(self):
        resp = self.client.post(reverse("trip_length_distribution:time"), {
            "Minimum": 10,
            "Maximum": 5,
            "intervals": 3
        })
        self.assertContains(resp, "Maximum must be greater than Minimum")

    def test_full_flow_session_and_frequency(self):
        # step 1: valid setup
        resp = self.client.post(reverse("trip_length_distribution:time"), {
            "Minimum": 0,
            "Maximum": 10,
            "intervals": 2
        })
        self.assertEqual(resp.status_code, 200)
        # session should now have data
        session = self.client.session
        self.assertIn("arrayOfTime", session)
        self.assertIn("numberOfIntervals", session)

        # step 2: post frequencies
        resp2 = self.client.post(reverse("trip_length_distribution:validation"), {
            "time0": 5,
            "time1": 5
        }, follow=True)
        # expect redirect to output or error if octave not configured
        self.assertIn(resp2.status_code, (200, 302))
