import uuid

from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class BaseModel(models.Model):
    """ BaseModel is used for generating UUID for models pk field """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class ImageField(ProcessedImageField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.format = "JPEG"
        self.options = {"quality": 90}

