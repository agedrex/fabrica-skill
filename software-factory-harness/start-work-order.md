# Fase de Inicio de la Orden de Trabajo

## Propósito
Reunir el contexto suficiente para implementar correctamente antes de escribir código.

## Flujo de trabajo

### 1. Retomar o inicializar el directorio de ejecución

Primero verificá si ya existe `scratch/wo-execution/WO-<number>/`.

- **Si existe:** retomá desde los archivos de ejecución existentes y continuá desde la fase actual del checklist.
- **Si no existe:** inicializalo:

```bash
bash .cursor/skills/software-factory/scripts/init-wo-execution.sh \
  --work-order-number "<number>" \
  --work-order-title "<title>"
```

La inicialización crea:
- **`checklist.md`** — checklist de ejecución
- **`context.md`** — metadatos de la orden de trabajo, documentos vinculados y contexto de entrega
- **`implementation-plan.md`** — plan de implementación
- **`review-log.md`** — log de revisión

No vuelvas a ejecutar la inicialización sobre un directorio de orden de trabajo existente, salvo que el usuario apruebe explícitamente reemplazar los archivos de ejecución.

### 2. Protocolo del checklist

Completá el checklist de forma incremental durante toda la ejecución. Marcá los ítems inmediatamente después de completarlos, agregá notas en tiempo real y registrá rutas de archivos y decisiones durante la implementación. No dejes las actualizaciones del checklist para el final. Cada fase termina con una única línea de certificación: tenés que marcarla antes de pasar a la fase siguiente.

**Protocolo de omisión:** si un ítem del checklist no aplica a esta orden de trabajo, escribí `[SKIP]` en el checkbox y dá el motivo en la línea inmediatamente inferior:
```
- [SKIP] E2E tests run/passing
  Skip reason: No UI changes in this work order — backend-only service refactor.
```

### 3. Recopilación de contexto

1. Usá los detalles de la orden de trabajo devueltos por `get_next_work_order` o `read_work_order` como alcance de ejecución.
2. Identificá los requisitos y blueprints vinculados a partir del contenido de la orden de trabajo.
3. Leé los documentos vinculados usando:
   - `read_requirement` / `search_requirements`
   - `read_blueprint` / `search_blueprints`
   - **CRÍTICO:** al leer blueprints, seguí todas las menciones `@BlueprintName` para leer los Component Blueprints referenciados. Los Feature Blueprints componen Component Blueprints, y necesitás ambos para entender el grafo completo de componentes y contratos.
4. Armá un breve resumen del contexto de ejecución:
   - resultados dentro del alcance según los requisitos
   - criterios de aceptación que deben cumplirse
   - ruta de arquitectura a partir de los blueprints (componentes/contratos)
   - Component Blueprints referenciados y sus componentes clave
5. Completá `context.md` con los identificadores de la orden de trabajo, un resumen de 1-2 oraciones de la solicitud del usuario y el ID + título del documento de requisitos/blueprint.
6. Confirmá con el usuario las dudas abiertas antes de implementar.

### 4. Escribir el plan de implementación

Escribí el plan de implementación en `scratch/wo-execution/WO-<number>/implementation-plan.md` (ver [writing-implementation-plans.md](writing-implementation-plans.md) para la estructura y la guía).

## Salvaguardas

- Mantené los mensajes concisos y operativos.
- Vinculá siempre las verificaciones de implementación y de finalización con el alcance de la orden de trabajo, los criterios de aceptación de los requisitos y la arquitectura del blueprint.
- Usá `.cursor/skills/review/SKILL.md` para la revisión de código (linting, alineación con el blueprint, arquitectura y convenciones).
- Usá `.cursor/skills/testing/SKILL.md` para el orden de ejecución de pruebas y los flags de los comandos.

## Por qué importa

Los requisitos son la fuente de verdad de la finalización (lo que debe ser cierto), mientras que los blueprints definen el enfoque técnico (cómo debe implementarse). Empezar bien implica capturar ambos de forma explícita, para que el código y las pruebas puedan rastrearse hasta los criterios de aceptación y la arquitectura desde el principio.
