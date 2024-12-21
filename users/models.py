from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from io import BytesIO
import boto3
import logging
import uuid
from django.conf import settings

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(upload_to="profile_photos/", blank=True, null=True)
    bio = models.TextField(max_length=200, null=True)
    location = models.CharField(max_length=50, null=True)
    is_client = models.BooleanField(default=True, null=True)
    is_freelancer = models.BooleanField(default=False, null=True)
    freelancer_verified = models.BooleanField(default=False, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.photo:
            try:
                image = Image.open(self.photo)

                webp_image_io = BytesIO()
                image.save(webp_image_io, format="WEBP", quality=85)
                webp_image_io.seek(0)

                unique_filename = f"profile_photos/{uuid.uuid4()}.webp"

                s3 = boto3.client("s3", region_name=settings.AWS_S3_REGION_NAME)
                s3.upload_fileobj(
                    webp_image_io,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    unique_filename,
                    ExtraArgs={"ContentType": "image/webp"},
                )

                original_filename = self.photo.name

                self.photo = unique_filename
                super().save(*args, **kwargs)

                s3.delete_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=original_filename
                )

            except Exception as e:
                raise RuntimeError(f"Error converting image to webp: {e}")

    def __str__(self):
        return f"{self.user.username}'s Profile"
