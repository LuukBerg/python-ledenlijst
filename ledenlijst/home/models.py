from django.db import models

# Create your models here.


class Member(models.Model):
    firstname = models.CharField(max_length=254)
    lastname = models.CharField(max_length=254)
    email = models.EmailField(primary_key=True, unique=True)
