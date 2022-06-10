import glob
import os

from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, SimpleTestCase

from apps.announcement.models import Announcement


class AnnouncementTests(TestCase):
    @classmethod
    def setUp(self):

        self.user = User.objects.create(
            id= 1,
            username='author',
            email='author@test.com',
            password ='qazxcvbnm',
        )
        image = SimpleUploadedFile("C:/Users/ibrah/Desktop/image_training/Testing/non_meme_image/IMG_ART_co (136).jpg",
                                   b"file_content", content_type="image/jpg")
        Announcement.objects.create(title ='Arts Completion',created_by = self.user, Description='please participate', image=image)


    def test_announcement(self):
        announcement = Announcement.objects.get(created_by = User.objects.get(id=1))
        expected_announcement_title = announcement.title
        self.assertEquals(expected_announcement_title,'Arts Completion')
    def test_announcementimage(self):
        announcement = Announcement.objects.get(created_by = User.objects.get(id=1))
        expected_announcement_title = announcement.image
        self.assertEquals(expected_announcement_title,announcement.image)


