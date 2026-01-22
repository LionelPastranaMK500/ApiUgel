# IEAPI/models/debate.py
from django.db import models
from .curso import Curso
from .asignacion_rol import PersonalPeriodo
from .matricula import Matricula

class DebateTema(models.Model):
    """
    Foros de discusión. Incluye descripción para plantear el tema de debate.
    """
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="debates")
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, help_text="Instrucciones o contexto del debate") 
    
    creador_personal = models.ForeignKey(PersonalPeriodo, on_delete=models.PROTECT, null=True, blank=True)
    creador_alumno = models.ForeignKey(Matricula, on_delete=models.PROTECT, null=True, blank=True)
    
    cerrado = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "debate_tema"

class DebatePost(models.Model):
    """
    Intervenciones. El contenido es el núcleo de la comunicación.
    """
    tema = models.ForeignKey(DebateTema, on_delete=models.CASCADE, related_name="posts")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="respuestas")
    
    autor_personal = models.ForeignKey(PersonalPeriodo, on_delete=models.PROTECT, null=True, blank=True)
    autor_alumno = models.ForeignKey(Matricula, on_delete=models.PROTECT, null=True, blank=True)
    
    contenido = models.TextField() 
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "debate_post"