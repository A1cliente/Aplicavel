from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('mototaxista', 'Mototaxista'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)
    telefone = models.CharField(max_length=15, blank=True)

class Corrida(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='corridas_cliente')
    mototaxista = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='corridas_mototaxista')
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('pendente', 'Pendente'), ('aceita', 'Aceita'), ('finalizada', 'Finalizada')], default='pendente')
    data = models.DateTimeField(auto_now_add=True)

class Localizacao(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.usuario.username} - {self.latitude}, {self.longitude}'



class Motoboy(models.Model):
    username = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return self.username
