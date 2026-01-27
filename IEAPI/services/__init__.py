# IEAPI/services/__init__.py
from .configuracion_service import procesar_identidad_ie, obtener_detalle_ie
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
from .auditoria_service import registrar_evento_critico
from .seguridad_service import validar_vinculo_institucional
from .transicion_service import procesar_finalizacion_grado
from .niveles_service import obtener_niveles_institucion, gestionar_niveles_institucion

__all__ = [
    "registrar_nuevo_perfil", "actualizar_perfil", "obtener_perfil_por_slug",
    "cambiar_estado_usuario", "verificar_disponibilidad_dni",
    "designar_personal_a_periodo", "proyectar_planilla_personal",
    "evolucionar_malla", "validar_y_congelar_malla", 
    "agregar_curso_a_malla_vigente", "proyectar_malla_a_seccion",
    "ejecutar_matricula", "configurar_esquema_evaluacion", "calcular_promedio_final",
    "registrar_asistencia_seccion", "generar_deuda_estudiante", "registrar_pago_efectivo",
    "listar_personal_administracion", "listar_alumnos_administracion", 
    "registrar_evento_critico", "validar_vinculo_institucional",
    "procesar_finalizacion_grado", "procesar_identidad_ie", "obtener_detalle_ie",
    "obtener_niveles_institucion", "gestionar_niveles_institucion"
    
]