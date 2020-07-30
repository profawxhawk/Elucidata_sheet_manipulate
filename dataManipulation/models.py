from django.db import models

class File(models.Model):
    File = models.FileField(upload_to='documents//%Y/%m/%d/')
    