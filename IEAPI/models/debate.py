# IEAPI/models/debate.py
from django.db import models
from .curso import Curso
from .asignacion_rol import PersonalPeriodo
from .matricula import Matricula

class DebateTema(models.Model):
    """
    Hilo de discusión académica dentro de un curso.
    Optimizado con índices y campos de auditoría temporal.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="debates")
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(help_text="Contexto o disparador del debate") 
    
    creador_personal = models.ForeignKey(PersonalPeriodo, on_delete=models.PROTECT, null=True, blank=True)
    creador_alumno = models.ForeignKey(Matricula, on_delete=models.PROTECT, null=True, blank=True)
    
    cerrado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True) 

    class Meta:
        db_table = "debate_tema"
        ordering = ["-creado_en"]
        indexes = [
            models.Index(fields=["curso"], name="idx_debate_curso"),
            models.Index(fields=["cerrado", "creado_en"], name="idx_debate_status"),
        ]

    def __str__(self):
        return f"{self.titulo} · {self.curso}"

class DebatePost(models.Model):
    """
    Intervenciones en el tema. Soporta árbol de respuestas (parent).
    """
    tema = models.ForeignKey(DebateTema, on_delete=models.CASCADE, related_name="posts")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="respuestas")
    
    autor_personal = models.ForeignKey(PersonalPeriodo, on_delete=models.PROTECT, null=True, blank=True)
    autor_alumno = models.ForeignKey(Matricula, on_delete=models.PROTECT, null=True, blank=True)
    
    contenido = models.TextField() 
    creado_en = models.DateTimeField(auto_now_add=True)
    editado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "debate_post"
        ordering = ["creado_en"]
        indexes = [
            models.Index(fields=["tema", "creado_en"], name="idx_post_tema_time"),
            models.Index(fields=["parent"], name="idx_post_parent_hilo"),
        ]

    def __str__(self):
        return f"Post {self.id} en {self.tema_id}"