import datetime as dt
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@testing.com'
    birthday = dt.date(year=1997, month=6, day=4)

    def test_signup_page_status(self):
        response =  self.client.get('/users/signup')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            birthday=self.birthday
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        self.assertEqual(get_user_model().objects.all()[0].birthday, self.birthday)


class UserEditTests(TestCase):
    username = 'newuser'
    email = 'newuser@testing.com'
    birthday = dt.date(year=1997, month=6, day=4)

    def setUp(self):
        self.new_user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            birthday=self.birthday
        )

        self.client.force_login(user=self.new_user)

    def test_edit_user_page_status(self):
        response =  self.client.get('/users/profile')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('user_profile'))
        self.assertTemplateUsed(response, 'registration/user_edit.html')
    
    def test_edit_form(self):
        response = self.client.post(reverse('user_profile'), {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'newmail@test.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(get_user_model().objects.all()[0].first_name, 'First Name')
        self.assertEqual(get_user_model().objects.all()[0].last_name, 'Last Name')
        self.assertEqual(get_user_model().objects.all()[0].email, 'newmail@test.com')
