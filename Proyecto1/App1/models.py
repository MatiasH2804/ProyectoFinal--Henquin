from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Ingreso(models.Model):
    CATEGORIAS_CHOICES = [
        ('sueldo', 'Sueldo'),
        ('otros', 'Otros'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES, default='otros')

class Gasto(models.Model):
    CATEGORIAS_CHOICES = [
        ('alimentos', 'Alimentos'),
        ('transporte', 'Transporte'),
        ('vivienda', 'Vivienda'),
        ('entretenimiento', 'Entretenimiento'),
        ('salud', 'Salud'),
        ('educacion', 'Educación'),
        ('varios', 'Varios'),
    ]
    MEDIO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('debito', 'Débito'),
        ('credito', 'Crédito'),
        ('transferencia', 'Transferencia'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100, choices=CATEGORIAS_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    medio_pago = models.CharField(max_length=100, choices=MEDIO_PAGO_CHOICES, default='efectivo')

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.imagen}"

@receiver(post_save, sender=User)
def create_user_avatar(sender, instance, created, **kwargs):
    if created:
        Avatar.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_avatar(sender, instance, **kwargs):
    instance.avatar.save()
