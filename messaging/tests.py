"""Tests for messaging app: inbox, sent, drafts, send, reply."""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

from messaging.models import Message


class MessageModelTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', first_name='A', last_name='B')
        self.bob = User.objects.create_user(username='bob')

    def test_message_str(self):
        m = Message.objects.create(sender=self.alice, recipient=self.bob, subject='Hi', body='hey')
        self.assertIn('Hi', str(m))

    def test_sender_initials(self):
        m = Message.objects.create(sender=self.alice, recipient=self.bob, subject='X', body='y')
        self.assertEqual(m.sender_initials(), 'AB')


class MessagingViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.alice = User.objects.create_user(username='alice', password='pw12345678', email='a@x.com')
        self.bob = User.objects.create_user(username='bob', password='pw12345678', email='b@x.com')
        Message.objects.create(sender=self.bob, recipient=self.alice,
                               subject='Hello Alice', body='Welcome', status='inbox')

    def test_messages_requires_login(self):
        r = self.client.get(reverse('messages'))
        self.assertEqual(r.status_code, 302)

    def test_inbox_shows_received_messages(self):
        self.client.login(username='alice', password='pw12345678')
        r = self.client.get(reverse('messages'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Hello Alice')

    def test_send_message_creates_inbox_copy_for_recipient(self):
        self.client.login(username='alice', password='pw12345678')
        r = self.client.post(reverse('send_message'), {
            'recipient_id': self.bob.pk, 'subject': 'Test', 'body': 'Body text',
        })
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Message.objects.filter(sender=self.alice, recipient=self.bob,
                                               subject='Test', status='sent').exists())
        self.assertTrue(Message.objects.filter(sender=self.alice, recipient=self.bob,
                                               subject='Test', status='inbox').exists())

    def test_send_rejects_empty_body(self):
        self.client.login(username='alice', password='pw12345678')
        r = self.client.post(reverse('send_message'), {
            'recipient_id': self.bob.pk, 'subject': 'X', 'body': '',
        })
        self.assertEqual(r.status_code, 400)

    def test_reply_creates_thread_message(self):
        self.client.login(username='alice', password='pw12345678')
        msg = Message.objects.filter(recipient=self.alice).first()
        r = self.client.post(reverse('reply_message', args=[msg.pk]),
                             {'subject': 'Re: Hello Alice', 'body': 'Thanks!'})
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Message.objects.filter(sender=self.alice, recipient=self.bob,
                                               body='Thanks!').exists())
