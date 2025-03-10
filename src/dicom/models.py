from django.db import models

from src.core.models import BaseModel


# Create your models here.
class Image_Upload(BaseModel):
    image = models.ImageField(upload_to="dicom_images/")

    def __str__(self):
        return f"Dicom Image {self.id} uploaded at {self.uploaded_at}"
