from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    generos = [
        ("F", "Feminino"),
        ("M", "Masculino"),
        ("O", "Outro"),
    ]

    nome_completo = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    genero = models.CharField(max_length=1, choices=generos, blank=True, null=True)
    cargo = models.CharField(
        max_length=150,
    )

    USERNAME_FIELD = "username"  # ou 'email' se for esse o login
    REQUIRED_FIELDS = ["email", "nome_completo"]

    def __str__(self):
        return self.username


class RespostaSRQ(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data_resposta = models.DateTimeField(auto_now_add=True)
    respostas = models.JSONField()
    score = models.IntegerField()

    def __str__(self):
        return f"SRQ-20 de {self.usuario.email} - {self.data_resposta.date()}"
