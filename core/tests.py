"""Tests for core app: landing, dashboard, search."""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from teams.models import Team, Department


class LandingDashboardTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='u', password='pw12345678')

    def test_landing_public(self):
        r = self.client.get(reverse('landing'))
        self.assertEqual(r.status_code, 200)

    def test_dashboard_requires_login(self):
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 302)

    def test_dashboard_loads(self):
        self.client.login(username='u', password='pw12345678')
        r = self.client.get(reverse('dashboard'))
        self.assertEqual(r.status_code, 200)


class SearchViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='u', password='pw12345678')
        self.dept = Department.objects.create(name='Engineering')
        Team.objects.create(name='Searchable Team', department=self.dept,
                            description='unique-string-zxq')

    def test_search_requires_login(self):
        r = self.client.get(reverse('search') + '?q=test')
        self.assertEqual(r.status_code, 302)

    def test_search_finds_team(self):
        self.client.login(username='u', password='pw12345678')
        r = self.client.get(reverse('search') + '?q=Searchable')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Searchable Team')

    def test_search_finds_department(self):
        self.client.login(username='u', password='pw12345678')
        r = self.client.get(reverse('search') + '?q=Engineering')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Engineering')

    def test_empty_query_renders_blank_state(self):
        self.client.login(username='u', password='pw12345678')
        r = self.client.get(reverse('search'))
        self.assertEqual(r.status_code, 200)
