from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase

from apps.complaint.models import Complaint , Feedback


class ComplaintTests(TestCase):
    @classmethod
    def setUp(self):

        self.user = User.objects.create(
            id= 1,
            username='author@test.com',
            email='author@test.com',
            password ='qazxcvbnm',
        )
        Complaint.objects.create(title =' new topic',created_by = self.user, Description='please add new topic')
        self.admin = User.objects.create(
            id=2,
            username='author2@test.com',
            email='author2@test.com',
            password='qazxcvbnm',
        )
        Feedback.objects.create(complaint=Complaint.objects.get(id=1), Description='ok we will', created_by=self.admin)

    def test_text(self):
        complaint = Complaint.objects.get(created_by = User.objects.get(id=1))
        expected_complaint_title = complaint.title
        self.assertEquals(expected_complaint_title,' new topic')

        feedback = Feedback.objects.get(complaint__created_by=User.objects.get(id=1))
        expected_feedback_Description = feedback.Description
        self.assertEquals(expected_feedback_Description, 'ok we will')

