from pathlib import Path

from django.test import TestCase

from user.models import User


# Create your tests here.
class InsertImagesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name="testUser", email="test@teste.com", password="123")
        self.login = self.client.post(data={"email": "test@teste.com", "password": "123"}, path="/api/v1/login")
        self.test_image_path = "app/static/test_image/one/8_jpg.rf.9f7540c6621d939078db38bd0eea9e1f.jpg"
        self.test_multi_images_path = ["app/static/test_image/multi/8_jpg.rf.9f7540c6621d939078db38bd0eea9e1f.jpg", "app/static/test_image/multi/7_jpg.rf.53c6f23558e598de89401d263a7a232f.jpg"]

    def test_SendOneImage(self):

        with open(self.test_image_path, "rb") as image_file:
            data = {
                "image": image_file,
                "user": self.user.id
            }

            res = self.client.post(data=data,path="/api/v1/app/image/upload", headers={"Authorization": "Bearer " + self.login.json()["access"]})

            self.assertEqual(res.status_code, 201)

    def test_SendManyImages(self):
        with open(self.test_multi_images_path[0], "rb") as image1, open(self.test_multi_images_path[1], "rb") as image2:
            data = {
                "multiImages": [image1, image2],
                "user": self.user.id
            }

            res = self.client.post(data=data, path="/api/v1/app/image/multi/upload",
                                   headers={"Authorization": "Bearer " + self.login.json()["access"]})

            self.assertEqual(res.status_code, 201)