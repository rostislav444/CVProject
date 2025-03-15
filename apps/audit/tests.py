from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from apps.audit.models import RequestLog


class RequestLogMiddlewareTests(TestCase):
    """Tests for the RequestLog middleware functionality."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_request_logging(self):
        """Test that requests are properly logged."""
        # Make a request to the home page
        response = self.client.get(reverse("main:cv_list"))
        self.assertEqual(response.status_code, 200)

        # Verify that the request was logged
        logs = RequestLog.objects.all()
        self.assertEqual(logs.count(), 1)

        # Verify log data
        log = logs.first()
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, reverse("main:cv_list"))

    def test_authenticated_user_logging(self):
        """Test that authenticated user requests are properly logged."""
        # Login the test user
        self.client.login(username="testuser", password="testpassword")

        # Make a request to the home page
        response = self.client.get(reverse("main:cv_list"))
        self.assertEqual(response.status_code, 200)

        # Verify that the request was logged with the user
        logs = RequestLog.objects.all()
        self.assertEqual(logs.count(), 1)

        # Verify log data including user
        log = logs.first()
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, reverse("main:cv_list"))
        self.assertEqual(log.user, self.user)

    def test_multiple_requests(self):
        """Test that multiple requests are properly logged."""
        # Make multiple requests
        urls = [
            reverse("main:cv_list"),
            reverse("audit:recent_requests"),
            "/admin/",
        ]

        for url in urls:
            self.client.get(url)

        # Verify that all requests were logged
        logs = RequestLog.objects.all()
        self.assertEqual(logs.count(), len(urls))


class RecentRequestsViewTests(TestCase):
    """Tests for the RecentRequestsView."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()

        # Create more than 10 request logs to test pagination
        for i in range(15):
            RequestLog.objects.create(
                method="GET",
                path=f"/test/{i}/",
            )

    def test_recent_requests_view(self):
        """Test that the recent requests view displays logs correctly."""
        response = self.client.get(reverse("audit:recent_requests"))
        self.assertEqual(response.status_code, 200)

        # Verify that the view contains logs
        self.assertIn("requests", response.context)

        # Verify that only 10 most recent logs are returned
        logs = response.context["requests"]
        self.assertEqual(len(logs), 10)

        # Verify that logs are ordered by timestamp (most recent first)
        for i in range(len(logs) - 1):
            self.assertGreaterEqual(logs[i].timestamp, logs[i + 1].timestamp)
