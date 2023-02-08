from django.test import TestCase
from django.contrib.auth.models import User
from app.models import StudySessionModel

class StudySessionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        StudySessionModel.objects.create(title="test",text="helloworld",start_time = "2022-11-7 5:10:11",duration="5 hr",address="clemons",author = user)
    def test_title_label(self):
        studysession = StudySessionModel.objects.get(id=1)
        field_label = studysession._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_text_label(self):
        studysession = StudySessionModel.objects.get(id=1)
        field_label = studysession._meta.get_field('text').verbose_name
        self.assertEqual(field_label, 'text')

    def test_starttime_label(self):
        studysession = StudySessionModel.objects.get(id=1)
        field_label = studysession._meta.get_field('start_time').verbose_name
        self.assertEqual(field_label, 'start time')

    def test_duration_label(self):
        studysession = StudySessionModel.objects.get(id=1)
        field_label = studysession._meta.get_field('duration').verbose_name
        self.assertEqual(field_label, 'duration')

    def test_address_label(self):
        studysession = StudySessionModel.objects.get(id=1)
        field_label = studysession._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'address')

    def test_user_label(self):
        studysession = StudySessionModel.objects.get(id=1)
        field_label = studysession._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_object_title_and_author(self):
        studysession = StudySessionModel.objects.get(id=1)
        expected_object_title_and_author = f'{studysession.title} | {studysession.author}'
        self.assertEqual(str(studysession), expected_object_title_and_author)

    def test_get_absolute_url(self):
        studysession = StudySessionModel.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(studysession.get_absolute_url(), '/app/list/')