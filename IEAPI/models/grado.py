from django.db import models

class Grado(models.Model):
    """
    Catálogo de grados alineado con Perú:
    - Inicial:     3 años (3, 4, 5) → proponemos nombres "3 años", "4 años", "5 años"
    - Primaria:    6 grados (1° a 6°)
    - Secundaria:  5 grados (1° a 5°)
    - Superior:    opcional (duración varía), aquí lo dejamos abierto
    """
    class Nivel(models.TextChoices):
        INICIAL     = "inicial", "Inicial"
        PRIMARIA    = "primaria", "Primaria"
        SECUNDARIA  = "secundaria", "Secundaria"
        SUPERIOR    = "superior", "Superior"

    nivel = models.CharField(max_length=12, choices=Nivel.choices)
    nombre = models.CharField(max_length=30)               # ej: "3 años", "1°", "2°", ...
    orden = models.PositiveSmallIntegerField()             # para ordenar dentro del nivel

    class Meta:
        db_table = "grado"
        unique_together = (("nivel", "nombre"),)
        ordering = ["nivel", "orden"]

    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_display()})"