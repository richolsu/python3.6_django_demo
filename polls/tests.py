import datetime
import unittest

from django.utils import timezone
from django.test import *
from django.contrib.auth.models import User

from .models import Question


def data_for():
    return 3;


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class IndexViewTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='admin')
        user.set_password('dalian2014')
        user.save()

    def test_call_view_denies_anonymous(self):
        sample = data_for()
        print(sample)
        response = self.client.get('/admin/polls/question/', follow=True)
        self.assertRedirects(response, '/admin/login/?next=/admin/polls/question/')

    def test_call_view_loads(self):
        self.client.login(user='admin', password='dalian2014')  # defined in fixture or with factory in setUp()
        response = self.client.get('/admin/polls/question/')
        self.assertEqual(response.status_code, 302)

    def test_home_view(self):
        user_login = self.client.login(username='admin', password='dalian2014')
        self.assertTrue(user_login)
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)

    # def test_call_view_fails_blank(self):
    #     self.client.login(username='user', password='test')
    #     response = self.client.post('/url/to/view', {}) # blank data dictionary
    #     self.assertFormError(response, 'form', 'some_field', 'This field is required.')
    #     # etc. ...
    #
    # def test_call_view_fails_invalid(self):
    #     # as above, but with invalid rather than blank data in dictionary
    #
    # def test_call_view_fails_invalid(self):
    #     # same again, but with valid data, then
    #     self.assertRedirects(response, '/contact/1/calls/')


suite = unittest.TestSuite()

suite.addTest(IndexViewTest('test_call_view_denies_anonymous'))
suite.addTest(IndexViewTest('test_home_view'))

runner = unittest.TextTestRunner()
runner.run(suite)

