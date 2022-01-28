import datetime as dt

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import List, Bullet

class ListTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='new_test_user',
            email='test@test.com',
            birthday=dt.date(year=1997, month=6, day=4)
        )

        self.client.force_login(user=self.user)

        self.list = List.objects.create(
            title='Test List',
            author=self.user
        )

        self.bullet_1 = Bullet.objects.create(
            title='Test Bullet',
            list=self.list,
            is_completed=False
        )
    
    def test_list_string_representation(self):
        self.assertEqual(str(self.list), self.list.title)

    def test_bullet_string_representation(self):
        self.assertEqual(str(self.bullet_1), self.bullet_1.title)

    def test_list_get_absolute_url(self):
        self.assertEqual(self.list.get_absolute_url(), '/lists/1')

    def test_bullet_get_absolute_url(self):
        self.assertEqual(self.bullet_1.get_absolute_url(), '/lists/1')

    def test_article_content(self):
        self.assertEqual(f'{self.list.title}', 'Test List')
        self.assertEqual(f'{self.list.author}', 'new_test_user')

    def test_bullet_content(self):
        self.assertEqual(f'{self.bullet_1.title}', 'Test Bullet')
        self.assertEqual(f'{self.bullet_1.list}', 'Test List')

    def test_list_list_view(self):
        response =  self.client.get('/lists/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test List')
        self.assertTemplateUsed(response, 'list_list.html')

        response = self.client.get(reverse('list_list'))
        self.assertEqual(response.status_code, 200)

    def test_list_create_view(self):
        response = self.client.get('/lists/create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_create.html')

        response = self.client.get(reverse('list_create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('list_create'), {
            'title': 'New title'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(List.objects.all().count(), 2)

    def test_list_update_view(self):
        response = self.client.get('/lists/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_edit.html')

        response = self.client.get(reverse('list_edit', args='1'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('list_edit', args='1'), {
            'Save': 'Save',
            'title-1': 'Updated bullet',
            'bullet-1': 'Checked'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bullet.objects.all()[0].title, 'Updated bullet')
        self.assertEqual(Bullet.objects.all()[0].is_completed, True)

    def test_bullet_add(self):

        response = self.client.post(reverse('list_edit', args='1'), {
            'Add': 'Add',
            'new_bullet_title': 'New bullet'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bullet.objects.all().count(), 2)

    def test_list_delete_view(self):
        response = self.client.get('/lists/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'list_delete.html')

        response = self.client.get(reverse('list_delete', args='1'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('list_delete', args='1'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(List.objects.all().count(), 0)
        self.assertEqual(Bullet.objects.all().count(), 0)

    def test_bullet_delete_view(self):
        response = self.client.get('/lists/bullet/1/delete')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bullet_delete.html')

        response = self.client.get(reverse('bullet_delete', args='1'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('list_delete', args='1'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Bullet.objects.all().count(), 0)


