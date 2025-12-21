from django.db import models
from django.conf import settings

class Conversacion(models.Model):
    """
    Conversación privada. Puede ser 1–1 (dos usuarios) o grupal (n usuarios).
    """
    nombre = models.CharField(max_length=120, blank=True, default="")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversacion"

    def __str__(self):
        return self.nombre or f"Conversación {self.id}"


class ConversacionMiembro(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="miembros")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversaciones")
    unido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversacion_miembro"
        unique_together = (("conversacion", "usuario"),)


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mensajes_enviados")
    texto = models.TextField(blank=True, default="")
    # archivos/links los puedes manejar luego en otra tabla
    leido_por = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="MensajeLectura",
        related_name="mensajes_leidos",
        blank=True,
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensaje"
        indexes = [
            models.Index(fields=["conversacion", "creado_en"], name="idx_msg_conver_time"),
            models.Index(fields=["autor"], name="idx_msg_autor"),
        ]
        ordering = ["creado_en"]


class MensajeLectura(models.Model):
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name="lecturas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensaje_lectura"
        unique_together = (("mensaje", "usuario"),)
from django.db import models
from django.conf import settings

class Conversacion(models.Model):
    """
    Conversación privada. Puede ser 1–1 (dos usuarios) o grupal (n usuarios).
    """
    nombre = models.CharField(max_length=120, blank=True, default="")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversacion"

    def __str__(self):
        return self.nombre or f"Conversación {self.id}"


class ConversacionMiembro(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="miembros")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversaciones")
    unido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conversacion_miembro"
        unique_together = (("conversacion", "usuario"),)


class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="mensajes_enviados")
    texto = models.TextField(blank=True, default="")
    # archivos/links los puedes manejar luego en otra tabla
    leido_por = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="MensajeLectura",
        related_name="mensajes_leidos",
        blank=True,
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensaje"
        indexes = [
            models.Index(fields=["conversacion", "creado_en"], name="idx_msg_conver_time"),
            models.Index(fields=["autor"], name="idx_msg_autor"),
        ]
        ordering = ["creado_en"]


class MensajeLectura(models.Model):
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE, related_name="lecturas")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leido_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mensaje_lectura"
        unique_together = (("mensaje", "usuario"),)
