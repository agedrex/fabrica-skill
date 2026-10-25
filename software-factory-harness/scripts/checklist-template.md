# Checklist de Ejecución de la Orden de Trabajo: WO-__WORK_ORDER_NUMBER__

**Número de Orden de Trabajo:** WO-__WORK_ORDER_NUMBER__
**Título de la Orden de Trabajo:** __WORK_ORDER_TITLE__
**Inicializada el (UTC):** __INITIALIZED_AT__

## Documentos Vinculados
- Documentos de requisitos revisados:
  - [ ] `read_requirement` completado para todos los requisitos vinculados
  - Notas:
- Documentos de blueprint revisados:
  - [ ] `read_blueprint` completado para todos los blueprints vinculados
  - [ ] Todas las menciones `@BlueprintName` seguidas y los blueprints referenciados leídos
  - Notas:

## Fase 1: Inicio / Recopilación de Contexto

### Pasos Requeridos
- [ ] Revisar la descripción de la orden de trabajo provista por la salida de la herramienta MCP
- [ ] Identificar los requisitos y blueprints vinculados
- [ ] Seguir todas las menciones `@BlueprintName` para leer los Component Blueprints referenciados
- [ ] Extraer los criterios de aceptación de los requisitos
- [ ] Identificar la ruta de arquitectura a partir de los blueprints (componentes, contratos, composición)
- [ ] `context.md` está completo con los metadatos de la orden de trabajo, un resumen de 1-2 oraciones de la solicitud del usuario y el ID + título del documento de requisitos/blueprint
- [ ] Hacerle preguntas aclaratorias al usuario sobre el alcance ambiguo

- [ ] **Certificación: Fase 1 completa — todos los ítems anteriores están hechos. Pasando a la Fase 2.**

## Fase 2: Planificación e Implementación

### Plan de Implementación
- [ ] Plan de implementación escrito en `implementation-plan.md` en este directorio (ver `.cursor/skills/software-factory/writing-implementation-plans.md`)
- [ ] Plan revisado con el usuario (si el alcance lo amerita)

### Implementación
- [ ] Implementar solo los cambios dentro del alcance
- [ ] Ejecutar el subagente `code-simplifier` sobre los archivos modificados
- [ ] Registrar abajo las decisiones clave de implementación a medida que se toman

### Notas
- Archivos modificados:
- Decisiones de implementación:

- [ ] **Certificación: Fase 2 completa — todos los ítems anteriores están hechos. Pasando a la Fase 3.**

## Fase 3: Verificación

Usá la skill `review` (`.cursor/skills/review/SKILL.md`) para ejecutar las tres dimensiones de revisión. Los resultados deben escribirse en el log de revisión (`review-log.md` en este directorio).

### Puertas de Calidad
- [ ] **Linting y verificación de tipos** — ejecutar con la guía linting-and-type-checking.md de la skill review
- [ ] **Alineación con el blueprint** — ejecutar con la guía blueprint-alignment.md de la skill review
- [ ] **Arquitectura y convenciones** — ejecutar con la guía architecture-and-conventions.md de la skill review
- [ ] No se introdujeron errores NUEVOS de linting/tipos (los errores preexistentes son aceptables)
- [ ] Ronda del log de revisión escrita en `review-log.md` con veredicto (REVISIÓN DEL AGENTE APROBADA ✅ o REVISIÓN DEL AGENTE SOLICITÓ CAMBIOS ❌)

### Pruebas
Ejecutá el plan de pruebas usando la skill de agente `testing`. Usá solo pruebas que no involucren LLM. Si las fallas son regresiones no relacionadas de la rama main, documentalas y no arregles pruebas ajenas.
- [ ] Pruebas unitarias de backend ejecutadas/aprobadas
- [ ] Pruebas de integración de backend ejecutadas/aprobadas
- [ ] Pruebas unitarias de frontend ejecutadas/aprobadas
- [ ] Pruebas E2E ejecutadas/aprobadas

### Validación de Requisitos y Blueprint
- [ ] Se cumplen todos los criterios de aceptación de la orden de trabajo y de los requisitos vinculados
- [ ] La arquitectura está alineada con los blueprints vinculados
- [ ] Cualquier desvío está documentado y revisado con el usuario

### Resumen de Resultados de Pruebas
- Unitarias:
- Integración:
- E2E:
- Otras:

- [ ] **Certificación: Fase 3 completa — todos los ítems anteriores están hechos. Pasando a la Fase 4.**

## Fase 4: Preparación para la Entrega

### Pasos Requeridos
- [ ] Todos los cambios previstos están commiteados
- [ ] Existe un pull request
- [ ] El título/descripción del PR menciona el número y el nombre de la orden de trabajo
- [ ] El PR incluye un resumen conciso + notas de verificación
- [ ] `context.md` está actualizado con la URL del pull request

### Información del PR
- URL del PR:
- Título del PR:

- [ ] **Certificación: Fase 4 completa — todos los ítems anteriores están hechos. Pasando a la Finalización.**

## Verificación Final de Completitud

- [ ] Todas las certificaciones de fase anteriores están completas
- [ ] El checklist está completamente llenado con evidencia
- [ ] El log de revisión está completo (`review-log.md`)
- [ ] Se siguió el plan de implementación (`implementation-plan.md`)
- [ ] Listo para llamar a `complete_work_order`

## Resumen Final

- Resultado:
- Riesgos remanentes:
- Tareas de seguimiento:
