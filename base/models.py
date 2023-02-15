from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Items(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.TextField(null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name