from django.db import models
from django.conf import settings
from .seccion import Seccion

class DebateTema(models.Model):
    """
    Hilo de debate dentro de una sección (foro).
    """
    seccion = models.ForeignKey(Seccion, on_delete=models.PROTECT, related_name="debates")
    titulo = models.CharField(max_length=200)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="debates_creados")
    cerrado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "debate_tema"
        indexes = [
            models.Index(fields=["seccion"], name="idx_debate_seccion"),
            models.Index(fields=["cerrado", "creado_en"], name="idx_debate_cerrado"),
        ]
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.titulo} · {self.seccion}"


class DebatePost(models.Model):
    """
    Publicación dentro de un tema. Soporta respuestas en árbol (parent opcional).
    """
    tema = models.ForeignKey(DebateTema, on_delete=models.PROTECT, related_name="posts")
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="posts_debate")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="respuestas")
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    editado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "debate_post"
        indexes = [
            models.Index(fields=["tema", "creado_en"], name="idx_post_tiempo"),
            models.Index(fields=["parent"], name="idx_post_parent"),
            models.Index(fields=["autor"], name="idx_post_autor"),
        ]
        ordering = ["creado_en"]

    def __str__(self):
        return f"Post {self.id} en {self.tema_id}"
