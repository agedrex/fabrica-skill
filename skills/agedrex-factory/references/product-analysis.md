# Análisis de producto como complemento, no como un modelo paralelo

La Fábrica es la fuente de verdad de la identidad y el ciclo de vida: Etapa → FRD (`documents` con
`kind=requirement`, `doc_type=feature`) → Feature Blueprint (`kind=blueprint`) → WO vinculado.
No crees entidades separadas de epic, story o feature que dupliquen estos registros.

Cuando sirva, incorporá las prácticas de análisis de producto en los artefactos existentes:

| Práctica | Lugar en La Fábrica |
|---|---|
| JTBD y necesidades del usuario | Problema/contexto del FRD y REQ/AC observables |
| Escenarios BDD | Criterios de aceptación del WO, trazados a los AC del FRD |
| Brief técnico del proyecto | Contratos del Blueprint y ADRs |
| Roadmap y capacidad | Planificación de la Etapa cuando existan datos reales |

Antes de cerrar un FRD, revisá la alineación estratégica, los AC faltantes de validación,
permisos y recuperación, la trazabilidad (cada AC pertenece a un solo REQ) y que los IDs sean
estables. La cobertura de una epic puede informar el límite de un requisito, pero nunca se
convierte en una entidad aparte en la base de datos. Preferí un WO vertical cuando un mismo
responsable de entrega abarca todo el stack; usá WOs por capas solo cuando la responsabilidad
realmente difiere. Marcá explícitamente las decisiones de producto que falten, en vez de inventar
comportamiento.

Conservá la atribución de la fuente al adaptar material de terceros. No copies plantillas
confidenciales o restringidas dentro de la skill. La ruta de referencia es `guides/flujo-de-trabajo.md`.
