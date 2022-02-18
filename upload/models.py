from django.db import models

class Document(models.Model):
    img = models.ImageField(upload_to='documents/', default='defo')
    msk = models.ImageField(upload_to='documents/', default='defo')