from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Baker(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='bakers/', blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Cake(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='cakes/', blank=True, null=True)
    baker = models.ForeignKey(Baker, on_delete=models.CASCADE, related_name='cakes')

    def __str__(self):
        return f'{self.name} - {self.price}'