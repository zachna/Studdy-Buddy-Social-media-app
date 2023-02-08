import datetime
from http.client import responses
from django.test.utils import setup_test_environment
from django.test import TestCase
from django.utils import timezone


from app.models import StudySessionModel
from django.urls import reverse
from django.contrib.auth.models import User
#class AddClassViewTest(TestCase):
 #   def get_t


import unittest
from django.test import Client


class SimpleTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.l = StudySessionModel.objects.all()
        self.user = User.objects.create_user(username="keyan",password="123")
    def test_get_class(self):
        response = self.client.get(reverse('get_class'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['response']),569)

    #def test_study_session_list(self):
    #    response = self.client.get(reverse('list'))
    #    self.assertEqual(response.status_code,200)
    #    self.assertEqual(len(response.context['formset']),len(self.l))
    

    def test_search(self):
        response = self.client.post(reverse('search'),{'name':'CS 1110'})
        self.assertContains(response,'CS 1110')

    def test_search_classname(self):
        response = self.client.post(reverse('search'),{'name':'Intro'})
        self.assertContains(response,'CS 1110')

    def test_search_instructor(self):
        response = self.client.post(reverse('search'),{'name':'Derrick'})
        self.assertContains(response,'CS 1010')

    def test_user(self):
        response = self.client.post(reverse('userSearch'),{'name1':'keyan'})
        self.assertContains(response,'keyan')

    def test_userlist(self):
        response = self.client.get(reverse('userList'))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.context['userList']),1)

    #def test_user2(self):
    #    response = self.client.post(reverse('userSearch'),{'name':'Fourth Year'})
    #    print(response)
        
    #def test_post_study_session(self):
    #    print(User.objects.all())
    #    user =  User.objects.get(username='keyan')
    #    studysession = StudySessionModel.objects.create(title="test",text="helloworld",start_time = "2022-11-7 5:10:11",duration="5 hr",address="clemons",author = user)
    #    response = self.client.get(reverse('post'))
    #    self.assertEqual(response.status_code,200)
    #    self.assertContains(response,studysession)

