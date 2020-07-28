from django.db import models

class File(models.Model):
    Name = models.CharField(max_length=255, blank=True)
    File = models.FileField(upload_to='documents//%Y/%m/%d/')
    