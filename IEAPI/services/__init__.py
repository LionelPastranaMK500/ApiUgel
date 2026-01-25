# IEAPI/services/__init__.py
from .configuracion_service import inicializar_institucion_maestra
from .usuario_service import (
    registrar_nuevo_perfil, actualizar_perfil, 
    obtener_perfil_por_slug, cambiar_estado_usuario, 
    verificar_disponibilidad_dni
)
from .personal_service import proyectar_planilla_personal
from .malla_service import (
    evolucionar_malla, validar_y_congelar_malla, 
    agregar_curso_a_malla_vigente
)
from .matricula_service import ejecutar_matricula
from .evaluacion_service import configurar_esquema_evaluacion
from .promedio_service import calcular_promedio_final
from .asistencia_service import registrar_asistencia_seccion
from .finanzas_service import generar_deuda_estudiante
from .consulta_service import listar_personal_administracion, listar_alumnos_administracion

__all__ = [
    "inicializar_institucion_maestra",
    "registrar_nuevo_perfil", "actualizar_perfil", "obtener_perfil_por_slug",
    "cambiar_estado_usuario", "verificar_disponibilidad_dni",
    "designar_personal_a_periodo", "proyectar_planilla_personal",
    "evolucionar_malla", "validar_y_congelar_malla", 
    "agregar_curso_a_malla_vigente", "proyectar_malla_a_seccion",
    "ejecutar_matricula", "configurar_esquema_evaluacion", "calcular_promedio_final",
    "registrar_asistencia_seccion", "generar_deuda_estudiante", "registrar_pago_efectivo",
    "listar_personal_administracion", "listar_alumnos_administracion"
]