
from django.contrib.auth.models import User

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, SimpleTestCase
from numpy import argmax

from apps.core.m_l_model import imagepredict
from apps.feed.models import PostFeed


class PostFeed_Valid_Tests(TestCase):
    @classmethod
    def setUp(self):

        self.user = User.objects.create(
            id= 1,
            username='author',
            email='author@test.com',
            password ='qazxcvbnm',
        )
        image = SimpleUploadedFile("C:/Users/ibrah/Desktop/image_training/Testing/meme_image/{51}.jpg",
                                   b"file_content", content_type="image/jpg")
        PostFeed.objects.create(body ='its a  meme image',created_by = self.user, feedimage=image)


    def test_feed_body(self):
        feed = PostFeed.objects.get(created_by = User.objects.get(id=1))
        expected_complaint_body = feed.body
        self.assertEquals(expected_complaint_body,'its a  meme image')
    def test_feed_valid_image(self):
        feed = PostFeed.objects.get(created_by = User.objects.get(id=1))
        expected_feed_image = feed.feedimage
        self.assertEquals(expected_feed_image,feed.feedimage)


class PostFeed_Meme_Tests(TestCase):
    @classmethod
    def setUp(self):

        self.user = User.objects.create(
            id= 1,
            username='author',
            email='author@test.com',
            password ='qazxcvbnm',
        )
        image = SimpleUploadedFile("C:/Users/ibrah/Desktop/image_training/Testing/meme_image/{51}.jpg",
                                   b"file_content", content_type="image/jpg")
        y = imagepredict("C:/Users/ibrah/Desktop/image_training/Testing/meme_image/{51}.jpg")
        if argmax(y) == 0 and float("{:.2f}".format((y[0][0] * 100))) > 85:
            print("The model has predicted the image is MEME" +
                  ' with a Confidence of ' + "{:.2f}".format((y[0][0] * 100)) + '%')
            PostFeed.objects.create(body='its a  meme image', created_by=self.user, feedimage='')
        else:
            PostFeed.objects.create(body ='its not MEME',created_by = self.user, feedimage=image)


    def test_feed_body(self):
        feed = PostFeed.objects.get(created_by = User.objects.get(id=1))
        expected_complaint_body = feed.body
        self.assertEquals(expected_complaint_body,'its a  meme image')
    def test_feed_meme_image(self):
        feed = PostFeed.objects.get(created_by = User.objects.get(id=1))
        expected_feed_image = feed.feedimage
        self.assertFalse(expected_feed_image,'')


class PostFeed_Selfie_Tests(TestCase):
    @classmethod
    def setUp(self):

        self.user = User.objects.create(
            id= 1,
            username='author',
            email='author@test.com',
            password ='qazxcvbnm',
        )
        image = SimpleUploadedFile("C:/Users/ibrah/Desktop/image_training/Testing/selfie_image/1781.jpg",
                                   b"file_content", content_type="image/jpg")
        y = imagepredict("C:/Users/ibrah/Desktop/image_training/Testing/selfie_image/1781.jpg")
        if argmax(y) == 1 and float("{:.2f}".format((y[0][1] * 100))) > 85:
            print("The model has predicted the image is a Selfie" +
                  ' with a Confidence of ' + "{:.2f}".format((y[0][1] * 100)) + '%')
            PostFeed.objects.create(body='its a  selfie image', created_by=self.user, feedimage='')
        else:
            PostFeed.objects.create(body ='its not Selfie',created_by = self.user, feedimage=image)


    def test_feed_body(self):
        feed = PostFeed.objects.get(created_by = User.objects.get(id=1))
        expected_complaint_body = feed.body
        self.assertEquals(expected_complaint_body,'its a  selfie image')
    def test_feed_selfie_image(self):
        feed = PostFeed.objects.get(created_by = User.objects.get(id=1))
        expected_feed_image = feed.feedimage
        self.assertFalse(expected_feed_image,'')

