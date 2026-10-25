# Fase de Completar la Orden de Trabajo

## Propósito
Ejecutar la verificación final, completar la orden de trabajo y capturar las notas de traspaso.

## Flujo de trabajo

1. **Revisar el checklist** — abrí `scratch/wo-execution/WO-<number>/checklist.md` y confirmá que:
   - Todas las certificaciones de fase están marcadas
   - No quedan ítems sin marcar (cada ítem está marcado o señalado como `[SKIP]` con un motivo)
   - Las notas y los resúmenes están completos

2. **Revisar el archivo de contexto** — abrí `scratch/wo-execution/WO-<number>/context.md` y confirmá que:
   - Los identificadores de la orden de trabajo están completos
   - El resumen de la solicitud del usuario está capturado en 1-2 oraciones
   - El ID y el título del documento de requisitos y del blueprint están completos
   - La URL del pull request está actualizada

3. **Revisar el log de revisión** — abrí `scratch/wo-execution/WO-<number>/review-log.md` y confirmá que:
   - El veredicto de la última ronda es **REVISIÓN DEL AGENTE APROBADA ✅** (cero hallazgos bloqueantes)
   - Si el veredicto es **REVISIÓN DEL AGENTE SOLICITÓ CAMBIOS ❌**, resolvé los hallazgos bloqueantes y ejecutá otra ronda de revisión antes de continuar

4. **Verificar el estado de la entrega:**
   - Todos los archivos previstos están commiteados (`git status` limpio para el alcance previsto)
   - Existe un PR (usá la skill `create-pr` si hace falta)
   - El título/descripción del PR menciona el número y el nombre de la orden de trabajo

5. **Llamá a `complete_work_order`** para el número de orden de trabajo correspondiente con un resumen de:
   - Qué se entregó (alcance de la orden de trabajo)
   - El veredicto del log de revisión y el número de la ronda final
   - Resumen de los resultados de las pruebas
   - Cualquier riesgo remanente o tarea de seguimiento

## Por qué importa

Completar no es solo "el código está listo". Es la prueba de que se siguió el checklist, de que la revisión convergió en una aprobación y de que el trabajo está listo para la revisión humana. Capturar los detalles del traspaso en la misma fase evita la pérdida de contexto después de la transición de estado.
