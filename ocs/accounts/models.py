from django.db import models
from django.contrib.auth.models import User
from provider.models import Provider
from franchise.models import Franchise

# Create your models here.
class OCSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    rfc = models.CharField(max_length=12)
    num_ss = models.CharField(max_length=12)
    direccion = models.CharField(max_length=200)
