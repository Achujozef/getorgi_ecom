from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='imagestore/')

    def __str__(self):
        return self.image.name