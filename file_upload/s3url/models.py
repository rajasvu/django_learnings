from django.db import models

# Create your models here.

class S3File(models.Model):
    """
    Test model to verify file handling
    """
    file = models.ImageField(verbose_name="image-file", upload_to = 'media_files')
