from http import HTTPStatus
from django.contrib.auth.models import User
from django.test import TestCase


class LoginTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='tester')
        self.user.set_password('I_Test_Th1ngs')
        self.user.save()

    def test_good_credentials(self):
        params = {
            'username': self.user.username,
            'password': 'I_Test_Th1ngs',
        }
        response = self.client.post('/account/login/', params, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_bad_password(self):
        params = {
            'username': self.user.username,
            'password': 'randompass',
        }
        response = self.client.post('/account/login/', params, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_bad_credentials(self):
        params = {
            'username': 'intruder_alert',
            'password': 'dASFdsa32da#!2d',
        }
        response = self.client.post('/account/login/', params, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def tearDown(self) -> None:
        self.user.delete()


class RegisterTest(TestCase):

    def setUp(self) -> None:
        self.registration_params = {
            'username': 'registration_test',
            'email': '',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': '',
            'password2': '',
        }

    def test_correct_input(self):
        self.registration_params['email'] = 'tester@testing.com'
        self.registration_params['password1'] = 'a1A!s2S@d3D#'
        self.registration_params['password2'] = 'a1A!s2S@d3D#'

        response = self.client.post(
            '/account/register/',
            self.registration_params,
            follow=True
        )

        new_user = User.objects.get(username=self.registration_params['username'])
        self.assertIsNotNone(new_user)

    def test_invalid_email(self):
        self.registration_params['email'] = 'tester'
        self.registration_params['password1'] = 'a1A!s2S@d3D#'
        self.registration_params['password2'] = 'a1A!s2S@d3D#'

        response = self.client.post(
            '/account/register/',
            self.registration_params,
            follow=True
        )

        new_user = User.objects.filter(username=self.registration_params['username'])
        self.assertFalse(new_user.exists())

    def test_wrong_password_confirmation(self):
        self.registration_params['email'] = 'tester'
        self.registration_params['password1'] = 'a1A!s2S@d3D#'
        self.registration_params['password2'] = 'oops_not_good!'

        response = self.client.post(
            '/account/register/',
            self.registration_params,
            follow=True
        )

        new_user = User.objects.filter(username=self.registration_params['username'])
        self.assertFalse(new_user.exists())

    def tearDown(self) -> None:
        try:
            created_user = User.objects.get(username=self.registration_params['username'])
            created_user.delete()

        except User.DoesNotExist:
            pass


class LogoutTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='tester')
        self.user.set_password('I_Test_Th1ngs')
        self.user.save()
        self.client.login(username='tester', password='I_Test_Th1ngs')

    def test_logged_in_user(self):
        response = self.client.get(
            '/account/logout/',
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logged_out_user(self):
        self.client.logout()
        response = self.client.get(
            '/account/logout/',
            follow=True
        )
        self.assertContains(
            response,
            r'<a href="/account/login/">Log in</a>',
            status_code=HTTPStatus.OK
        )

    def tearDown(self) -> None:
        self.user.delete()
